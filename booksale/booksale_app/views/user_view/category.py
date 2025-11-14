# views.py
from django.shortcuts import render, get_object_or_404
from ...models import Category, Product

# Hiển thị danh sách tất cả category
def category_view(request):
    categories = Category.objects.all()
    return render(request, 'user_temp/product/category.html', {'categories': categories})

def category_detail_view(request, category_name):
    category = Category.objects.get(category_name=category_name)
    products = category.product_set.all()

    return render(request, 'user_temp/product/category_detail.html', {
        'category': category,
        'products': products
    })
def product_detail_user(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]
    return render(request, 'user_temp/product/product_detail.html', {
        'product': product,
        'related_products': related_products,
    })


