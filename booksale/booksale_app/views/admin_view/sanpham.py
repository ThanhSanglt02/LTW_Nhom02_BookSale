from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from booksale_app.models import Product, Category, Genre, Publisher
from booksale_app.forms import ProductForm


@login_required(login_url='login')
def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    genres = Genre.objects.all()
    publishers = Publisher.objects.all()

    # ---- Filter tìm kiếm và chọn danh mục ----
    search = request.GET.get('search', '')
    if search:
        products = products.filter(product_name__icontains=search)

    category = request.GET.get('category', '')
    if category:
        products = products.filter(category_id=category)

    genre = request.GET.get('genre', '')
    if genre:
        products = products.filter(genre__id=genre)

    publisher = request.GET.get('publisher', '')
    if publisher:
        products = products.filter(publisher_id=publisher)

    # ---- Filter theo giá ----
    price_range = request.GET.get('price_range')

    if price_range == "1":
        products = products.filter(sell_price__lt=100000)

    elif price_range == "2":
        products = products.filter(sell_price__gte=100000, sell_price__lte=200000)

    elif price_range == "3":
        products = products.filter(sell_price__gt=200000)

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
    return render(request, 'admin_temp/product/product_edit.html', {'form': form, 'title': 'Chỉnh sửa sản phẩm'})

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


from booksale_app.models import Product  # Đảm bảo Product được import


def product_bulk_delete(request):
    if request.method == 'POST':
        product_ids = request.POST.getlist('product_ids')

        if product_ids:
            # 1. Tìm TẤT CẢ PRODUCT ID ĐÃ XUẤT HIỆN TRONG ORDER_ITEM
            protected_product_ids = Order_Item.objects.values_list('product_id', flat=True).distinct()

            # 2. Lọc ra những ID không bị bảo vệ
            deletable_ids = list(set(product_ids) - set(protected_product_ids))

            if deletable_ids:
                # 3. CHỈ xóa những sản phẩm KHÔNG BỊ RÀNG BUỘC
                Product.objects.filter(id__in=deletable_ids).delete()
                messages.success(request, f"Đã xóa thành công {len(deletable_ids)} sản phẩm.")

            # 4. Cảnh báo về những sản phẩm không thể xóa
            if len(deletable_ids) < len(product_ids):
                not_deleted_count = len(product_ids) - len(deletable_ids)
                messages.warning(request,
                                 f"Không thể xóa {not_deleted_count} sản phẩm do chúng đã được đặt hàng và đang được bảo vệ bởi ràng buộc cơ sở dữ liệu.")

        return redirect('product_list')

    return redirect('product_list')