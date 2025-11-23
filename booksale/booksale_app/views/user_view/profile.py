from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from booksale_app.models import Customer
from ..authen_view import group_required
from django.conf import settings

@login_required(login_url="/accounts/login/kh/")
@group_required('KH', login_url="/accounts/login/kh/") 
def profile(request):
    """Hiển thị trang profile của user"""
    customer, created = Customer.objects.get_or_create(
        user=request.user,
        defaults={
            'cust_name': request.user.get_full_name() or request.user.username,
            'email': request.user.email or '',
            'phone': '',
            'address': '',
        }
    )

    if request.method == 'POST':
        # Cập nhật thông tin cơ bản
        customer.email = request.POST.get('email', customer.email)
        customer.phone = request.POST.get('phone', customer.phone)
        customer.address = request.POST.get('address', customer.address)
        customer.dob = request.POST.get('birthday', customer.dob)

        
        
        # Cập nhật avatar (nếu có file upload)
        if 'avatar' in request.FILES:
            customer.avatar = request.FILES['avatar']
        
        # Lưu tất cả thay đổi
        customer.save()
        
        return redirect('profile')  # Redirect về trang profile (không có ?edit=true)

    context = {
        'customer': customer,
        'user': request.user
    }
    
    return render(request, 'user_temp/profile/profile.html', context)

