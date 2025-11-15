from django.views import View
from django.shortcuts import render
from booksale_app.models import Category, Product
from django.contrib.auth.decorators import login_required
from ..authen_view import group_required

# Create your views here.

# def home_view(request):
#     return render(request, 'user_temp/home.html')

# class HomeView(View):
#     def get(self, request):
from django.views import View
from django.shortcuts import render

# Create your views here.

def home_view(request):
    user = request.user
    is_kh = False

    if user.is_authenticated:
        is_kh = user.groups.filter(name="KH").exists()

    # Lấy tất cả categories
    categories = Category.objects.all()[:3]  # Lấy 3 categories đầu tiên
    
    # Lấy products theo từng category (4 sản phẩm đầu tiên mỗi category)
    categories_with_products = []
    for category in categories:
        products = Product.objects.filter(category=category)[:4]  # Lấy 4 sản phẩm đầu tiên
        categories_with_products.append({
            'category': category,
            'products': products
        })
    
    context = {
        'categories': categories,
        'categories_with_products': categories_with_products,
        "is_kh": is_kh,
    }
    
    return render(request, 'user_temp/home.html', context)

# class HomeView(View):
#     def get(self, request):
#         return render(request, 'home.html')