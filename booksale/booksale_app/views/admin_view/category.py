from django.shortcuts import render, redirect, get_object_or_404
from booksale_app.models import Category, Product
from django.contrib import messages

def category_list(request):
    search = request.GET.get("search", "")

    categories = Category.objects.all()

    if search:
        categories = categories.filter(category_name__icontains=search)

    context = {
        "categories": categories,
    }
    return render(request, "admin_temp/category/category_list.html", context)

def category_add(request):
    if request.method == "POST":
        category_name = request.POST.get('category_name', '').strip()
        description = request.POST.get('description', '').strip()

        if category_name:
            Category.objects.create(category_name=category_name, description=description)
            # Thông báo thành công nếu muốn, ví dụ session
            request.session['success'] = "Đã thêm danh mục thành công ✅"
            return redirect('category_list')
        else:
            error = "Tên danh mục không được để trống"
            return render(request, 'admin_temp/category/category_form.html',
                          {'category': None, 'error': error, 'title': 'Thêm danh mục'})

    return render(request, 'admin_temp/category/category_form.html', {'category': None, 'title': 'Thêm danh mục'})


def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.name = request.POST.get('category_name')
        category.description = request.POST.get('description')
        category.save()
        return redirect('category_list')
    return render(request, 'admin_temp/category/category_form.html', {'category': category})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "Danh mục đã được xóa thành công.")
        return redirect('category_list')
    # GET request → render template xác nhận xóa
    return render(request, 'admin_temp/category/category_delete.html', {'category': category})

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
#    products = category.product_set.all()  # giả sử mối quan hệ FK Product -> Category
    products = Product.objects.filter(category=category)
    if request.method == "POST":
        description = request.POST.get("description", "")
        category.description = description
        category.save()
        return redirect('category_detail', pk=category.pk)  # reload page sau khi lưu

    return render(request, 'admin_temp/category/category_detail.html', {
        'category': category,
        'products': products,
    })


def category_bulk_delete(request):
    """
    Xử lý yêu cầu POST để xóa nhiều danh mục cùng lúc.
    """
    # 1. Kiểm tra phải là phương thức POST không
    if request.method == 'POST':
        # 2. Lấy danh sách ID từ các checkbox đã chọn
        # 'category_ids' là thuộc tính name của các input checkbox trong HTML
        category_ids = request.POST.getlist('category_ids')

        # 3. Thực hiện xóa hàng loạt trong cơ sở dữ liệu
        if category_ids:
            # Lọc các đối tượng Category có ID nằm trong danh sách và gọi hàm .delete()
            Category.objects.filter(id__in=category_ids).delete()

            # (Tùy chọn) Thêm thông báo thành công
            # messages.success(request, f"Đã xóa thành công {len(category_ids)} danh mục.")

        # 4. Chuyển hướng người dùng trở lại trang danh sách danh mục
        return redirect('category_list')

        # Nếu truy cập bằng GET, chuyển hướng về trang danh sách (hoặc trả về lỗi 405)
    return redirect('category_list')