from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from ..forms import CreateUserForm
from django.contrib.auth.models import Group

from django.contrib.auth.views import LoginView,LogoutView
from django.shortcuts import redirect

## Điều chỉnh lại việc chức năng Login theo nhóm role
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
         ## truyền tham số cấu hình cho Login View ở đây là extra_context --> nó là 1 thuộc tính được truyền vào LoginView và { "required_group": "KH" } được gán vào thuộc tính đó
        ## required_group: KH, NVBH, NVTK
        ## Có yêu cầu nhóm và user không thuộc nhóm đó --> từ chối đăng nhập --> return message lỗi
        # required_group có thể là 1 string hoặc 1 list
        required_group = self.extra_context.get("required_group", None)
        if required_group:
            ## check required_group là chuỗi
            if isinstance(required_group, str):
                allowed = user.groups.filter(name=required_group).exists()
            ## check required_group là list
            else:
                allowed = user.groups.filter(name__in=required_group).exists()

        if not allowed:
            logout(self.request)
            return self.render_to_response({
                **self.get_context_data(form=form),
                "error": "Tài khoản không hợp lệ"
            })
        # pass -> cho phép đăng nhập
        return super().form_valid(form)
    
## Điều chỉnh lại việc chức năng logout và điều hướng màn hình theo nhóm role
class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        # Lưu kết quả vì sau khi logout user sẽ mất
        is_nvbh = False
        is_nvtk = False
        if user.is_authenticated:
            is_nvbh = user.groups.filter(name="NVBH").exists()
            is_nvtk = user.groups.filter(name="NVTK").exists()


        # Gọi logout gốc của Django
        response = super().dispatch(request, *args, **kwargs)

        # Redirect theo nhóm
        if is_nvbh or is_nvtk:
            return redirect('/accounts/login/staff')
        else:
            return redirect('/')

        return response

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
    if user.groups.filter(name='NVTK').exists():
        return redirect('/employee/inventory_overview/')

    # Không thuộc nhóm nào → báo lỗi
    return redirect('/accounts/login/')

    
def register_view(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Tự động thêm user vào nhóm KH
            group = Group.objects.get(name='KH')
            user.groups.add(group)

            return redirect('/accounts/login/kh')
    return render(request, 'registration/register.html', {'form': form})


