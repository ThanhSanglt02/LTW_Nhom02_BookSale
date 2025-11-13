import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from booksale_app.models import Product, Category, Genre, Publisher
from booksale_app.forms import ProductForm

from django.conf import settings



@login_required(login_url='login')
def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    genres = Genre.objects.all()
    publishers = Publisher.objects.all()

    # ---- Thêm bộ lọc ở đây ----
    search = request.GET.get('search', '')
    if search:
        products = products.filter(product_name__icontains=search)

    category = request.GET.get('category', '')
    if category:
        products = products.filter(category_id=category)

    genre = request.GET.get('genre', '')
    if genre:
        products = products.filter(genre_id=genre)

    publisher = request.GET.get('publisher', '')
    if publisher:
        products = products.filter(publisher_id=publisher)
    # --------------------------

    context = {
        'products': products,
        'categories': categories,
        'genres': genres,
        'publishers': publishers,
    }
    return render(request, 'admin_temp/product/product_list.html', context)
@login_required(login_url='login')
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)

            # Lưu ảnh đại diện (nếu có)
            if 'image' in request.FILES:
                product.image = request.FILES['image']

            product.save()
            form.save_m2m()  # Lưu M2M (genre)

            messages.success(request, "✅ Tạo sản phẩm thành công.")
            return redirect('product_list')
        else:
            print("❌ FORM LỖI:", form.errors)
            messages.error(request, "❌ Dữ liệu không hợp lệ, vui lòng kiểm tra lại.")
    else:
        form = ProductForm()

    return render(
        request,
        'admin_temp/product/product_form.html',
        {'form': form, 'title': 'Thêm sản phẩm'}
    )

@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            form.save_m2m()
            messages.success(request, "Cập nhật sản phẩm thành công.")
            return redirect('product_list')
        else:
            messages.error(request, "Dữ liệu không hợp lệ.")
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin_temp/product/product_form.html', {'form': form, 'title': 'Chỉnh sửa sản phẩm'})

# Xóa sản phẩm
@login_required(login_url='login')
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.genre_item_set.all().delete()
        product.delete()
        messages.success(request, "Sản phẩm đã được xóa thành công.")
        return redirect('product_list')
    return render(request, 'admin_temp/product/product_delete.html', {'product': product})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if not product.image:
        product.image_url = '/static/images/default.png'
    else:
        product.image_url = product.image.url

    return render(request, 'admin_temp/product/product_detail.html', {'product': product})
