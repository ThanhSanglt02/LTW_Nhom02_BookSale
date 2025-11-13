from django.shortcuts import render, redirect
from django.contrib import messages
from booksale_app.models import Product  # hoặc tên model sản phẩm của bạn
from django.utils import timezone
from django.db import connection

def inventory_import(request):
    """
    Trang phiếu nhập kho: chọn sản phẩm, nhập số lượng và lưu vào DB
    """
    products = Product.objects.all()  # lấy danh sách sản phẩm để chọn

    if request.method == "POST":
        product_id = request.POST.get("product")
        quantity = request.POST.get("quantity")

        # kiểm tra dữ liệu hợp lệ
        if not product_id or not quantity:
            messages.error(request, "Vui lòng nhập đầy đủ thông tin.")
        else:
            try:
                # Giả sử bạn có bảng inventory_imports hoặc inventory_log trong DB
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO inventory_imports (product_id, quantity, import_date)
                        VALUES (%s, %s, %s)
                    """, [product_id, quantity, timezone.now()])
                messages.success(request, "Nhập kho thành công!")
                return redirect('inventory_list')
            except Exception as e:
                messages.error(request, f"Lỗi khi lưu dữ liệu: {e}")

    return render(request, 'employee/inventory/inventory_import.html', {
        'products': products,
        'page': 'inventory_import'

    })
