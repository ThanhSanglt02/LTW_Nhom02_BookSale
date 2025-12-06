from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from decimal import Decimal
from datetime import datetime
from django.contrib.auth.decorators import login_required
from booksale_app.views.authen_view import group_required
from booksale_app.models import ExportOrder, ExportOrder_Item, Product, Employee, Order, Order_Item
from booksale_app.forms import ExportOrderForm
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os
from django.conf import settings

# LIST
@login_required(login_url="/accounts/login/staff/")
@group_required("NVTK", login_url="/accounts/login/staff/")
def export_order_list(request):
    exports = ExportOrder.objects.all().order_by("-id")
    return render(request, "employee/inventory/inventory_export/inventory_export_list.html", {
        "export_orders": exports,
        "page": "inventory_export",
    })
# CREATE
@login_required(login_url="/accounts/login/staff/")
@group_required("NVTK", login_url="/accounts/login/staff/")
def export_order_create(request):
    today = datetime.now().strftime("%d/%m/%Y")
    employee = request.user.employee
    selected_order = None
    products = None

    if request.method == "POST" and "order_id" in request.POST and "qty_submit" not in request.POST:
        # Người dùng chỉ chọn đơn hàng => load sản phẩm
        order_id = request.POST["order_id"]
        selected_order = Order.objects.get(id=order_id)
        products = selected_order.order_item_set.all()

    elif request.method == "POST" and "qty_submit" in request.POST:
        # Người dùng submit phiếu xuất
        order_id = request.POST["order_id"]
        selected_order = Order.objects.get(id=order_id)
        order_items = selected_order.order_item_set.all()

        # Kiểm tra tồn kho trước khi tạo phiếu xuất
        insufficient_stock = False
        for item in order_items:
            qty = item.quantity
            if item.product.quantity < qty:
                insufficient_stock = True
                break

        if insufficient_stock:
            # Nếu không đủ hàng, hiển thị thông báo lỗi và không tạo phiếu xuất
            messages.error(request, "Tồn kho không đủ để xuất tất cả sản phẩm.")
            return render(request, "employee/inventory/inventory_export/inventory_export_form.html", {
                "orders": Order.objects.all(),
                "selected_order": selected_order,
                "products": products,
                "edit_mode": False,
                "today": today,
                "employee": employee,
            })

        with transaction.atomic():
            export = ExportOrder.objects.create(
                order=selected_order,
                employee=request.user.employee,
                total_amount=0
            )

            total = Decimal(0)

            for item in order_items:
                qty = item.quantity
                price = item.unit_price

                ExportOrder_Item.objects.create(
                    exportOrder=export,
                    product=item.product,
                    quantity=qty,
                    unit_price=price,
                    total_price=qty * price
                )

                # Trừ kho
                item.product.quantity -= qty
                item.product.save()

                total += qty * price

            export.total_amount = total
            export.save()
            print(f"Export Order Total: {export.total_amount}")

        messages.success(request, "Tạo phiếu xuất thành công")
        return redirect("inventory_export_list")

    return render(request, "employee/inventory/inventory_export/inventory_export_form.html", {
        "orders": Order.objects.all(),
        "selected_order": selected_order,
        "products": products,
        "edit_mode": False,
        "today": today,
        "employee": employee,
    })


# DETAIL
@login_required(login_url="/accounts/login/staff/")
@group_required("NVTK", login_url="/accounts/login/staff/")
def export_order_detail(request, pk):
    export = get_object_or_404(ExportOrder, pk=pk)
    items = ExportOrder_Item.objects.filter(exportOrder=export)

    return render(request, "employee/inventory/inventory_export/inventory_export_detail.html", {
        "export": export,
        "items": items,
    })

def order_detail_api(request, id):
    try:
        order = Order.objects.get(id=id)
    except Order.DoesNotExist:
        return JsonResponse({"error": "Order not found"}, status=404)

    # customer
    customer = order.customer

    # get items
    items = Order_Item.objects.filter(order=order)

    item_list = []
    total_amount = 0

    for item in items:
        line_total = item.quantity * item.unit_price
        total_amount += line_total

        item_list.append({
            "product": item.product.product_name,
            "quantity": item.quantity,
            "price": float(item.unit_price),
            "total": float(line_total)
        })

    data = {
        "customer": {
            "name": customer.cust_name,
            "phone": customer.phone,
            "address": customer.address,
        },
        "items": item_list,
        "total_amount": total_amount
    }

    return JsonResponse(data)


# DELETE
@login_required(login_url="/accounts/login/staff/")
@group_required("NVTK", login_url="/accounts/login/staff/")
def export_order_delete(request, pk):
    # Lấy đối tượng ExportOrder theo pk
    export = get_object_or_404(ExportOrder, pk=pk)

    # Lấy tất cả các ExportOrder_Item liên quan
    items = ExportOrder_Item.objects.filter(exportOrder=export)

    # Thực hiện các thay đổi trong một giao dịch (transaction)
    with transaction.atomic():
        # Trả lại số lượng sản phẩm trong kho
        for item in items:
            item.product.quantity += item.quantity
            item.product.save()

        # Xóa tất cả các ExportOrder_Item liên quan
        items.delete()

        # xóa ExportOrder
        export.delete()

    # Thông báo thành công
    messages.success(request, "Xóa phiếu xuất thành công")

    # Chuyển hướng lại danh sách phiếu xuất
    return redirect("inventory_export_list")

# EXPORT PDF
@login_required(login_url="/accounts/login/staff/")
@group_required("NVTK", login_url="/accounts/login/staff/")
def export_order_export_pdf(request, pk):
    export_order = get_object_or_404(ExportOrder, pk=pk)
    items = ExportOrder_Item.objects.filter(exportOrder=export_order)

    # Đăng ký font tiếng Việt (dùng NotoSans hoặc DejaVuSans)
    font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'NotoSans-Regular.ttf')
    pdfmetrics.registerFont(TTFont('NotoSans', font_path))

    # Tạo response PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="phieu_xuat_{export_order.id}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='VNTitle', fontName='NotoSans', fontSize=16, alignment=1))
    styles.add(ParagraphStyle(name='VNText', fontName='NotoSans', fontSize=11, leading=14))

    elements = []

    # Tiêu đề
    elements.append(Paragraph(f"<b>PHIẾU XUẤT KHO #{export_order.id}</b>", styles['VNTitle']))
    elements.append(Spacer(1, 12))

    #Thông tin phiếu
    info_data = [
        ["Ngày xuất:", export_order.export_date.strftime("%d/%m/%Y %H:%M")],
        ["Nhân viên:", export_order.employee.emp_name],
        ["Đơn hàng:", f"#{export_order.order.id}"],
        ["Khách hàng:", export_order.order.customer.cust_name],
        ["Số điện thoại:", export_order.order.customer.phone],
        ["Địa chỉ:", export_order.order.customer.address],
    ]

    info_table = Table(info_data, colWidths=[120, 350])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'NotoSans'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 20))

    # Danh sách sản phẩm
    table_data = [["Sản phẩm", "Số lượng", "Đơn giá (VNĐ)", "Thành tiền (VNĐ)"]]
    for item in items:
        table_data.append([
            item.product.product_name,
            str(item.quantity),
            f"{float(item.unit_price):,.0f}",
            f"{float(item.total_price):,.0f}",
        ])
    table_data.append(["", "", "Tổng tiền:", f"{float(export_order.total_amount or 0):,.0f}"])

    table = Table(table_data, colWidths=[180, 80, 100, 100])
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'NotoSans'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
    ]))
    elements.append(table)

    # Chữ ký
    elements.append(Spacer(1, 30))
    signature = Table(
        [["Người lập phiếu", "Người nhận hàng", "Thủ kho"],
         ["(Ký và ghi rõ họ tên)", "(Ký và ghi rõ họ tên)", "(Ký và ghi rõ họ tên)"]],
        colWidths=[180, 180, 180]
    )
    signature.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'NotoSans'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    elements.append(signature)

    # Xuất file PDF
    doc.build(elements)
    return response