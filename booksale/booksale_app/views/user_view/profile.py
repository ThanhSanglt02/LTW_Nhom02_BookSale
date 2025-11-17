from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from booksale_app.models import Customer
from ..authen_view import group_required

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
    
    context = {
        'customer': customer,
        'user': request.user
    }
    
    return render(request, 'user_temp/profile/profile.html', context)

