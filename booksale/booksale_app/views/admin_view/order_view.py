from django.shortcuts import render, get_object_or_404
from booksale_app.models import Order, Customer, Order_Item

from booksale_app.utils import sum_price_order
# Create your views here.

def order_list(request):
    orders =  (Order.objects
            .select_related('customer')
            .order_by('-order_date')) # select_related('customer') để lấy luôn thông tin khách hàng
    order_data = []
    for order in orders:
        order_items = Order_Item.objects.select_related('product').filter(order=order)
        # Truyền vào danh sách giá * số lượng
        prices = [item.product.sell_price * item.quantity for item in order_items]
        total_amount = sum_price_order(prices)
        order_data.append({
            'order': order,
            'total_amount': total_amount
        })
    context = {
        'order_data': order_data
    }
    return render(request, 'admin_temp/order/order_list.html', context)

def order_detail(request, pk):
    # Lấy thông tin đơn hàng
    order = get_object_or_404(Order.objects.select_related('customer'), pk=pk)
    # Lấy các sản phẩm thuộc đơn hàng đó
    order_items = Order_Item.objects.select_related('product').filter(order=order)
    prices = [item.product.sell_price * item.quantity for item in order_items]
    total_amount = sum_price_order(prices)
    context = {
        'order': order,
        'order_items': order_items,
        'total_amount': total_amount
    }
    return render(request, 'admin_temp/order/order_detail.html', context)

def order_confirm(request, pk):
    # Lấy thông tin đơn hàng
    order = get_object_or_404(Order.objects.select_related('customer'), pk=pk)
    # Lấy các sản phẩm thuộc đơn hàng đó
    order_items = Order_Item.objects.select_related('product').filter(order=order)
    prices = [item.product.sell_price * item.quantity for item in order_items]
    total_amount = sum_price_order(prices)
    context = {
        'order': order,
        'order_items': order_items,
        'total_amount': total_amount
    }
    return render(request, 'admin_temp/order/order_confirm.html', context)


# def edit_order(request, pk = None):
#     if pk is not None:
#         publisher = get_object_or_404(Order, pk = pk)
#     else:
#         publisher = None

#     if request.method == 'POST':
#         form = PublisherForm(request.POST, instance=publisher)
#         if form.is_valid():
#             # luwu object vào db
#             # updated_publisher chứa thông tin mà cái Model Publisher nó return ở hàm __str__
#             updated_publisher = form.save()
#             if publisher is None:
#                 messages.success(request, "Publisher {} was created.".format(updated_publisher))
#             else: 
#                 messages.success(request, "Publisher {} was updated.".format(updated_publisher))
#             # mở lại trang publisher_edit với ID của publisher đã lưu. --> ban đầu chưa có pk thì sẽ đi vào đường dẫn publishers/new. Sau khi taoj mới sucess thì đường dẫn sẽ được cập nhật kèm theo pk thay vì None
#                     # và lúc này pk đã có nên nó sẽ lấy url publishers/<int:pk>/
#             return redirect("publisher_edit", updated_publisher.pk) #pk tương ứng với cột id trong db
#     else:
#         form = PublisherForm(instance=publisher)
#     return render(request, "form_example.html", {"method": request.method, "form": form})

# class HomeView(View):
#     def get(self, request):
#         return render(request, 'home.html')