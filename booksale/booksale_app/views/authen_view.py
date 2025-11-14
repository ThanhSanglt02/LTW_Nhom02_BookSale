from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from ..forms import CreateUserForm
from booksale_app.models import Order, Order_Item
from booksale_app.utils import sum_price_order

def group_required(group_name):
    def check_group(user):
        return user.groups.filter(name=group_name).exists()
    return user_passes_test(check_group, login_url='/accounts/login/')
        

@login_required
@group_required('KH')
def home_view(request):
    return render(request, 'user_temp/home.html')

# Bỏ Dashboard
@login_required
@group_required('NVBH')
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


# @login_required
# @group_required('NVTK', redirect_url='/home/')
# def sales_dashboard(request):
#     # chỉ Sales vào được
#     return render(request, 'sales_dashboard.html')


@login_required
def role_redirect_view(request):
    user = request.user
    if user.groups.filter(name='NVBH').exists():
        return redirect('/emp/order_list/')
    # elif user.groups.filter(name='KH').exists():
    #     return redirect('/warehouse/dashboard/')
    else:
        return redirect('/')
    
    
def register_view(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        print("cos loi xay ra")
    context = {'form': form}
    return render(request, 'register.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password') 
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'user or password is not correct!')
    return render(request, 'login_temp.html')

def logout_view(request):
    logout(request)
    return redirect('login')
