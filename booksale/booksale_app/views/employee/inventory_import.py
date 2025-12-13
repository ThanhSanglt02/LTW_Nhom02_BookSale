from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from booksale_app.forms import ImportOrderForm

from booksale_app.models import ImportOrder, ImportOrder_Item, Product, Supplier, Employee
from booksale_app.views.authen_view import group_required

# External libraries
from datetime import date
from decimal import Decimal
import os

# ReportLab imports for PDF
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from django.conf import settings



# LIST
@login_required(login_url="/accounts/login/staff/")
@group_required("NVTK", login_url="/accounts/login/staff/")
def import_order_list(request):
    orders = ImportOrder.objects.all().order_by("-import_date")

    return render(
        request,
        "employee/inventory/inventory_import/inventory_import_list.html",
        {
            "import_orders": orders,
            "page": "inventory_import",
        }
    )


# CREATE
@transaction.atomic
@login_required(login_url="/accounts/login/staff/")
@group_required("NVTK", login_url="/accounts/login/staff/")
def import_order_create(request):
    products = Product.objects.all()
    suppliers = Supplier.objects.all()
    today = date.today().strftime("%Y-%m-%d")

    form = ImportOrderForm()

    if request.method == "POST":
        form = ImportOrderForm(request.POST)

        product_ids = request.POST.getlist("product_id[]")
        quantities = request.POST.getlist("quantity[]")
        prices = request.POST.getlist("price[]")

        if form.is_valid():
            order = form.save(commit=False)

            # GÁN NHÂN VIÊN ĐÚNG KIỂU
            order.employee = request.user.employee
            order.total_amount = 0
            order.save()

            total = 0

            for i in range(len(product_ids)):
                if not product_ids[i]:
                    continue

                product = get_object_or_404(Product, id=product_ids[i])
                qty = quantities[i]

                # XỬ LÝ GIÁ HỢP LỆ
                price_str = prices[i].replace(".", "").replace(",", "")
                price = Decimal(price_str)
                item_total = qty * price

                ImportOrder_Item.objects.create(
                    importOrder=order,
                    product=product,
                    quantity=qty,
                    unit_price=price,
                    total_price=item_total,
                )

                product.quantity += qty
                product.save()

                total += item_total

            order.total_amount = total
            order.save()

            messages.success(request, "Tạo phiếu nhập kho thành công.")
            return redirect("inventory_import_list")

        else:
            print(form.errors)
            messages.error(request, "Dữ liệu không hợp lệ!")

    return render(
        request,
        "employee/inventory/inventory_import/inventory_import_form.html",
        {
            "import_form": form,
            "products": products,
            "suppliers": suppliers,
            "today": today,
            "title": "Tạo phiếu nhập kho",
            "page": "inventory_import",
        }
    )

# DETAIL
@login_required(login_url="/accounts/login/staff/")
@group_required("NVTK", login_url="/accounts/login/staff/")
def import_order_detail(request, pk):
    order = get_object_or_404(ImportOrder, pk=pk)
    items = ImportOrder_Item.objects.filter(importOrder=order)

    return render(
        request,
        "employee/inventory/inventory_import/inventory_import_detail.html",
        {
            "order": order,
            "items": items,
            "page": "inventory_import",
        }
    )

# DELETE
@transaction.atomic
@login_required(login_url="/accounts/login/staff/")
@group_required("NVTK", login_url="/accounts/login/staff/")
def import_order_delete(request, pk):
    order = get_object_or_404(ImportOrder, pk=pk)

    # Lấy toàn bộ item thuộc phiếu
    items = ImportOrder_Item.objects.filter(importOrder=order)

    # Hoàn tồn lại số lượng sản phẩm
    for item in items:
        product = item.product
        product.quantity -= item.quantity
        product.save()

    # Xoá toàn bộ chi tiết phiếu
    items.delete()

    # Xoá phiếu nhập
    order.delete()

    messages.success(request, "Xoá phiếu nhập thành công.")

    return redirect("inventory_import_list")

# PDF EXPORT
@login_required(login_url="/accounts/login/staff/")
@group_required("NVTK", login_url="/accounts/login/staff/")
def import_order_export_pdf(request, pk):
    order = get_object_or_404(ImportOrder, pk=pk)
    items = ImportOrder_Item.objects.filter(importOrder=order)

    # Đăng ký font tiếng Việt
    font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'NotoSans-Regular.ttf')
    pdfmetrics.registerFont(TTFont('NotoSans', font_path))

    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="phieu_nhap_{order.id}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='VNTitle', fontName='NotoSans', fontSize=16, alignment=1))
    styles.add(ParagraphStyle(name='VNText', fontName='NotoSans', fontSize=11, leading=14))

    elements = []
    elements.append(Paragraph(f"<b>PHIẾU NHẬP KHO #{order.id}</b>", styles['VNTitle']))
    elements.append(Spacer(1, 12))

    # Thông tin phiếu
    info_data = [
        ["Ngày nhập:", order.import_date.strftime("%d/%m/%Y %H:%M")],
        ["Nhà cung cấp:", order.supplier.sup_name],
        ["Nhân viên:", order.employee.emp_name],
    ]
    info_table = Table(info_data, colWidths=[120, 350])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'NotoSans'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 20))

    # Bảng sản phẩm
    table_data = [["Sản phẩm", "Số lượng", "Đơn giá (VNĐ)", "Thành tiền (VNĐ)"]]
    for item in items:
        table_data.append([
            item.product.product_name,
            str(item.quantity),
            f"{float(item.unit_price):,.0f}",
            f"{float(item.total_price):,.0f}"
        ])
    table_data.append(["", "", "Tổng tiền:", f"{float(order.total_amount):,.0f}"])

    table = Table(table_data, colWidths=[180, 80, 100, 100])
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'NotoSans'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    elements.append(table)

    doc.build(elements)
    return response