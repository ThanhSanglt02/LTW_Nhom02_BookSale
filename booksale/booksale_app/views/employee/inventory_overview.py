from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..authen_view import group_required
from django.db.models import Sum
from ..authen_view import group_required
from booksale_app.models import Product, Order_Item, ImportOrder_Item, ImportOrder

@login_required(login_url="/accounts/login/warehouse/")
@group_required('NVTK', login_url="/accounts/login/warehouse/") # Nếu user không thuộc NVTK → redirect về login/warehouse.
def inventory_list(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(product_name__icontains=query)

    data = []
    for p in products:
        # Đang giao dịch: các đơn chưa xác nhận hoặc chờ xác nhận
        in_transaction = (
            Order_Item.objects
            .filter(product=p, order__status='pending')
            .aggregate(total=Sum('quantity'))['total'] or 0
        )

        # Đang về kho: các phiếu nhập chưa xác nhận (giả sử cậu muốn tính như vậy)
        incoming = (
            ImportOrder_Item.objects
            .filter(product=p)
            .aggregate(total=Sum('quantity'))['total'] or 0
        )

        # Có thể bán = tồn kho - đang giao dịch (đảm bảo không âm)
        available = max(p.quantity - in_transaction, 0)

        data.append({
            'id': p.id,
            'name': p.product_name,
            'stock': p.quantity,
            'available': available,
            'in_transaction': in_transaction,
            'incoming': incoming,
            'sell_price': p.sell_price,
            'cost_price': p.cost_price,
        })


    return render(request, 'employee/inventory/inventory_list.html', {
        'products': data,
        'query': query,
        'page': 'inventory_list'
    })

def inventory_add(request):
    return HttpResponse("Trang thêm sản phẩm vào kho (chưa code).")

def inventory_edit(request, pk):
    return HttpResponse(f"Sửa sản phẩm có id = {pk} (chưa code).")

def inventory_delete(request, pk):
    return HttpResponse(f"Xóa sản phẩm có id = {pk} (chưa code).")