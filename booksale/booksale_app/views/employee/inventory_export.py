from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.db import connection
from booksale_app.models import Product

def inventory_export(request):
    """
    Trang phiếu xuất kho: chọn sản phẩm, nhập số lượng và lưu log
    """
    products = Product.objects.all()
    today = timezone.now()

    if request.method == "POST":
        product_id = request.POST.get("product")
        quantity = request.POST.get("quantity")
        note = request.POST.get("note", "")
        export_date = request.POST.get("export_date", today)

        if not product_id or not quantity:
            messages.error(request, "Vui lòng chọn sản phẩm và nhập số lượng.")
        else:
            try:
                quantity = int(quantity)
                product = Product.objects.get(id=product_id)

                if quantity > product.quantity:
                    messages.error(request, "Số lượng xuất vượt quá tồn kho.")
                else:
                    # Giảm tồn kho
                    product.quantity -= quantity
                    product.save()

                    # Lưu vào bảng log xuất kho
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            INSERT INTO inventory_exports (product_id, quantity, export_date, note)
                            VALUES (%s, %s, %s, %s)
                        """, [product_id, quantity, export_date, note])

                    messages.success(request, "Xuất kho thành công!")
                    return redirect('inventory_list')

            except Exception as e:
                messages.error(request, f"Lỗi khi xử lý: {e}")

    return render(request, 'employee/inventory/inventory_export.html', {
        'products': products,
        'today': today,
        'page': 'inventory_export'
    })
