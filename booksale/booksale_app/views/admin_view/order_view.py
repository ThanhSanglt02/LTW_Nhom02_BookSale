from django.shortcuts import render, get_object_or_404, redirect
from booksale_app.models import Order, Order_Item, Customer
from django.contrib import messages
from booksale_app.utils import sum_price_order
from django.contrib.auth.decorators import login_required
from ..authen_view import group_required
from booksale_app.forms import OrderForm, OrderSearchForm
from django.utils import timezone
from django.db.models import Q

# Create your views here.
@login_required(login_url="/accounts/login/staff/")
@group_required('NVBH', login_url="/accounts/login/staff/") # Nếu user không thuộc NVBH → redirect về login staff.
def order_list(request):
    order_data = []
    # Lấy dữ liệu từ form
    if 'submit_input' in request.GET:  # kiểm tra có submit không
        form = OrderSearchForm(request.GET)
        if form.is_valid():
            search_value = form.cleaned_data['search'] 
            # select_related('customer') để lấy luôn thông tin khách hàng
            orders = Order.objects.select_related('customer').filter(
                #lọc các đơn hàng mà tên khách hàng chứa "Nguyen"
                Q(customer__cust_name__icontains=search_value) |
                Q(customer__phone__icontains=search_value)
            ).order_by('-order_date')
    else:
        form = OrderSearchForm()
        orders = Order.objects.select_related('customer').order_by('-order_date')

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
        'order_data': order_data,
        'form': form
    }
    return render(request, 'admin_temp/order/order_list.html', context)

def order_list_waiting(request):
    order_data = []
    # Lấy dữ liệu từ form
    if 'submit_input' in request.GET:  # kiểm tra có submit không
        form = OrderSearchForm(request.GET)
        if form.is_valid():
            search_value = form.cleaned_data['search'] 
            # select_related('customer') để lấy luôn thông tin khách hàng
            orders = Order.objects.select_related('customer').filter(
                #lọc các đơn hàng mà tên khách hàng chứa "Nguyen"
                (Q(customer__cust_name__icontains=search_value) |
                Q(customer__phone__icontains=search_value)), status="confirmed"
            ).order_by('-order_date')
    else:
        form = OrderSearchForm()
        orders = Order.objects.select_related('customer').filter(status="pending").order_by('-order_date')

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
        'order_data': order_data,
        'form': form
    }
    return render(request, 'admin_temp/order/order_list_waiting.html', context)


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
    # Lấy danh sách item trong đơn hàng
    order_items = Order_Item.objects.select_related('product').filter(order=order)

    if request.method == "POST":
        order.status = "confirmed"
        order.save()

        # Cập nhật lại số lượng sản phẩm
        for item in order_items:
            product = item.product # kết nối với bảng Product thông qua khóa ngoại
            sold_quantity = item.quantity

            product.quantity = product.quantity - sold_quantity
            if product.quantity < 0:
                print(f"Không đủ sản phẩm: {product.name}")
                return redirect('order_detail', pk=order.id)
            product.save()
    return redirect('order_detail', pk=order.id)

@login_required(login_url="/accounts/login/staff/")
def order_cancel_status(request, pk):
    """Cập nhật trạng thái thành đã hủy"""
    if request.method == "POST":
        order = Order.objects.get(id=pk)
        order.status = "cancelled"
        order.save()

        return redirect('order_detail', pk=pk)
    

