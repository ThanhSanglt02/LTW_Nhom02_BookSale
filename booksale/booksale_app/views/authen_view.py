from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from ..forms import CreateUserForm
from booksale_app.models import Order, Order_Item
from booksale_app.utils import sum_price_order

from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

def home_view(request):
    return render(request, 'user_temp/home.html')

class RoleLoginView(LoginView):
    # Đây là tên file template mà LoginView sẽ dùng để render form login. --> Mỗi khi LoginView cần render template (GET ban đầu hoặc POST lỗi), nó sẽ load file này
    template_name = "registration/login.html"

    def get_context_data(self, **kwargs):
        #super().get_context_data(**kwargs): là hàm của LoginView. Nó trả về một dictionary chứa các biến template mà Django login view mặc định truyền xuống template.
        context = super().get_context_data(**kwargs)
        # Truyền URL action xuống template --> thêm key action_url vào biến context với value là path mà request gửi đi
        context['action_url'] = self.request.path  # Hoặc self.extra_context.get("action_url")
        # Truyền group (tuỳ chọn để hiển thị thông báo)
        context['required_group'] = self.extra_context.get("required_group", None)
        return context

    def form_valid(self, form):
        user = form.get_user()
        required_group = self.extra_context.get("required_group", None)

        if required_group and not user.groups.filter(name=required_group).exists():
            logout(self.request)
            return self.render_to_response({
                **self.get_context_data(form=form),
                "error": "Tài khoản không hợp lệ"
            })
        return super().form_valid(form)

def group_required(group_name, login_url=None):
    if login_url is None:
        login_url = '/accounts/login/'

    def check_group(user):
        return user.groups.filter(name=group_name).exists()
    return user_passes_test(check_group, login_url=login_url)


@login_required
def role_redirect_view(request):
    user = request.user
    # Nếu thuộc nhóm KH
    if user.groups.filter(name='KH').exists():
        return redirect('home')   # Home cho khách hàng

    # Nhân viên bán hàng
    if user.groups.filter(name='NVBH').exists():
        return redirect('/emp/order_list/')

    # Nhân viên thủ kho
    # if user.groups.filter(name='NVTK').exists():
    #     return redirect('warehouse_dashboard')

    # Không thuộc nhóm nào → báo lỗi
    return redirect('/accounts/login/')



# Bỏ Dashboard
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


