from django.shortcuts import render
from django.db import models
from booksale_app.models import Product, ExportOrder_Item, ImportOrder_Item


def inventory_overview(request):
    # Lấy từ khóa tìm kiếm và tab đang chọn
    search_query = request.GET.get('search', '').strip()
    tab = request.GET.get('tab', 'all')  # all / in / out

    # Lọc sản phẩm theo từ khóa
    if search_query:
        products = Product.objects.filter(product_name__icontains=search_query)
    else:
        products = Product.objects.all()

    # Dữ liệu tổng hợp kho
    inventory_data = []
    for product in products:
        total_imported = ImportOrder_Item.objects.filter(product=product).aggregate(
            total_imported=models.Sum('quantity'))['total_imported'] or 0

        total_sold = ExportOrder_Item.objects.filter(product=product).aggregate(
            total_sold=models.Sum('quantity'))['total_sold'] or 0

        stock = total_imported - total_sold
        available = stock if stock > 0 else 0
        low_stock_warning = stock < 2

        inventory_data.append({
            'product_code': product.id,
            'product_name': product.product_name,
            'total_imported': total_imported,
            'total_sold': total_sold,
            'stock': stock,
            'available': available,
            'sell_price': product.sell_price,
            'cost_price': product.cost_price,
            'low_stock_warning': low_stock_warning,
        })

    # ✅ Lọc theo tab
    if tab == 'in':  # Còn hàng
        inventory_data = [item for item in inventory_data if item['stock'] >= 2]
    elif tab == 'out':  # Hết hàng
        inventory_data = [item for item in inventory_data if item['stock'] < 2]

    context = {
        'inventory': inventory_data,
        'search_query': search_query,
        'active_tab': tab,
        "page": "inventory_list",
    }

    return render(request, 'employee/inventory/inventory_list.html', context)
