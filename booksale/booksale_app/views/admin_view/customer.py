from django.shortcuts import render, get_object_or_404
from booksale_app.models import Customer, Order, Order_Item
from django.contrib.auth.decorators import login_required
from ..authen_view import group_required

# Dnah sach khach hang
@login_required(login_url="/accounts/login/staff/")
@group_required('NVBH', login_url="/accounts/login/staff/") 
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'admin_temp/customer/customer_list.html', {"customers": customers})

# Lich su dat hang
@login_required(login_url="/accounts/login/staff/")
@group_required('NVBH', login_url="/accounts/login/staff/") 
def customer_order_history(request, pk):
    customer = customer = Customer.objects.get(pk=pk)

    # Lấy thông tin đơn hàng dựa vào id của customer
    orders = Order.objects.filter(customer=pk).order_by("-order_date")
    # # Lấy danh sách item trong đơn hàng
    # order_items = Order_Item.objects.select_related('product').filter(order=order)
    total_orders = orders.count()
    total_spent = sum(order.total_amount for order in orders)
    context = {
        "customer": customer,
        "orders": orders,
        "total_orders": total_orders,
        "total_spent": total_spent,
    }

    return render(request, 'admin_temp/customer/customer_order_history.html', context)