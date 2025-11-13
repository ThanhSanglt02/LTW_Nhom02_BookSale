from django.views import View
from django.shortcuts import render
from booksale_app.models import Category, Product

# Create your views here.

# def home_view(request):
#     return render(request, 'user_temp/home.html')

# class HomeView(View):
#     def get(self, request):
from django.views import View
from django.shortcuts import render

# Create your views here.

def home_view(request):
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
        'categories_with_products': categories_with_products
    }
    
    return render(request, 'user_temp/home.html', context)

# class HomeView(View):
#     def get(self, request):
#         return render(request, 'home.html')