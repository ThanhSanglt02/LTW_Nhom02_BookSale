from django.shortcuts import render, get_object_or_404, redirect
from booksale_app.models import Order, Order_Item
from django.contrib import messages
from booksale_app.utils import sum_price_order
from django.contrib.auth.decorators import login_required
from ..authen_view import group_required

# Create your views here.

@login_required(login_url="/accounts/login/staff/")
@group_required('NVBH', login_url="/accounts/login/staff/") # Nếu user không thuộc NVBH → redirect về login staff.
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

    # Chọn template theo trạng thái
    if order.status == "confirmed":
        template = 'admin_temp/order/order_detail.html'
    elif order.status == "cancelled":
        template = 'admin_temp/order/order_cancel.html'
    else:
        template = 'admin_temp/order/order_confirm.html'
    return render(request, template, context)

def order_confirm_status(request, pk):
    """Cập nhật trạng thái thành đã xác nhận"""
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        order.status = "confirmed"
        order.save()
        messages.success(request, f"Đơn hàng #{order.id} đã được xác nhận thành công.")
        return redirect('emp/detail', pk=order.id)
    return redirect('emp/detail', pk=order.id)


def order_cancel_status(request, pk):
    """Cập nhật trạng thái thành đã hủy"""
    if request.method == "POST":
        reason = request.POST.get("cancel_reason", "")
        order = Order.objects.get(id=pk)
        order.status = "cancelled"
        order.cancel_reason = reason
        order.save()

        return redirect('emp/detail', pk=pk)
    

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