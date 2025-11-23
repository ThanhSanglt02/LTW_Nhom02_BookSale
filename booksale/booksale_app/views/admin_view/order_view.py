from django.shortcuts import render, get_object_or_404, redirect
from booksale_app.models import Order, Order_Item
from django.contrib import messages
from booksale_app.utils import sum_price_order
from django.contrib.auth.decorators import login_required
from ..authen_view import group_required
from django.utils import timezone

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


@login_required(login_url="/accounts/login/staff/")
def order_detail(request, pk):
    # Lấy thông tin đơn hàng + customer
    order = get_object_or_404(Order.objects.select_related('customer'), pk=pk)

    # Lấy danh sách item trong đơn hàng
    order_items = Order_Item.objects.select_related('product').filter(order=order)

    # Tính tổng tiền
    prices = [item.product.sell_price * item.quantity for item in order_items]
    total_amount = sum_price_order(prices)


    # XỬ LÝ UPDATE (NẾU POST)
    if request.method == "POST":
        shipping_date = request.POST.get("shipping_date")
        note = request.POST.get("note")
        order_status = request.POST.get("order_status")

        # Gán lại giá trị vào model
        order.shipping_date = shipping_date
        order.note = note
        order.status = order_status

        order.save()

        # Redirect để tránh gửi lại form khi F5
        return redirect("emp/completed", pk=pk)

    # Truyền dữ liệu qua template
    context = {
        'order': order,
        'order_items': order_items,
        'total_amount': total_amount,
        'today': timezone.now().date(),
    }

    # TEMPLATE THEO STATUS
    if order.status == "confirmed":
        template = 'admin_temp/order/order_detail.html'
    elif order.status == "cancelled":
        template = 'admin_temp/order/order_cancel.html'
    elif order.status == "completed":
        template = 'admin_temp/order/order_completed.html'
    else:
        template = 'admin_temp/order/order_confirm.html'

    return render(request, template, context)


@login_required(login_url="/accounts/login/staff/")
def order_confirm_status(request, pk):
    """Cập nhật trạng thái thành đã xác nhận"""
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        order.status = "confirmed"
        order.save()
        messages.success(request, f"Đơn hàng #{order.id} đã được xác nhận thành công.")
        return redirect('order_detail', pk=order.id)
    return redirect('order_detail', pk=order.id)

@login_required(login_url="/accounts/login/staff/")
def order_cancel_status(request, pk):
    """Cập nhật trạng thái thành đã hủy"""
    if request.method == "POST":
        reason = request.POST.get("cancel_reason", "")
        order = Order.objects.get(id=pk)
        order.status = "cancelled"
        order.cancel_reason = reason
        order.save()

        return redirect('order_detail', pk=pk)
    
# @login_required(login_url="/accounts/login/staff/")
# def edit_order(request, pk = None):
#     if pk is not None:
#         order = get_object_or_404(Order, pk = pk)
#     else:
#         order = None

#     if request.method == 'POST':
#         form = OrderForm(request.POST, instance=order)
#         if form.is_valid():
#             # luwu object vào db
#             # updated_publisher chứa thông tin mà cái Model Publisher nó return ở hàm __str__
#             updated_order = form.save()
#             if order is None:
#                 messages.success(request, "Order {} was created.".format(updated_order))
#             else: 
#                 messages.success(request, "Order {} was updated.".format(updated_order))
#             # mở lại trang publisher_edit với ID của publisher đã lưu. --> ban đầu chưa có pk thì sẽ đi vào đường dẫn publishers/new. Sau khi taoj mới sucess thì đường dẫn sẽ được cập nhật kèm theo pk thay vì None
#                     # và lúc này pk đã có nên nó sẽ lấy url publishers/<int:pk>/
#             return redirect("publisher_edit", updated_order.pk) #pk tương ứng với cột id trong db
#     else:
#         form = OrderForm(instance=order)
#     return render(request, "form_example.html", {"method": request.method, "form": form})

# class HomeView(View):
#     def get(self, request):
#         return render(request, 'home.html')