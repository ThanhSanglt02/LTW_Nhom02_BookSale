from django.shortcuts import render, redirect, get_object_or_404
from booksale_app.models import Genre, Product , Genre_Item # Cần import cả Product
from django.contrib import messages
from django.db.models import ProtectedError  # Import ProtectedError để xử lý lỗi


# --- 1. Danh sách Thể loại (Genre List) ---
def genre_list(request):
    search = request.GET.get("search", "")
    genres = Genre.objects.all()

    if search:
        genres = genres.filter(genre_name__icontains=search)

    context = {
        "genres": genres,
        "search": search,
    }
    return render(request, "admin_temp/genre/genre_list.html", context)


# --- 2. Thêm Thể loại (Genre Add) ---
def genre_add(request):
    if request.method == "POST":
        genre_name = request.POST.get('genre_name', '').strip()
        description = request.POST.get('description', '').strip()

        if genre_name:
            Genre.objects.create(genre_name=genre_name, description=description)
            messages.success(request, f"Đã thêm thể loại '{genre_name}' thành công ✅")
            return redirect('genre_list')
        else:
            messages.error(request, "Tên thể loại không được để trống!")
            # Giữ lại dữ liệu đã nhập nếu có lỗi
            return render(request, 'admin_temp/genre/genre_form.html',
                          {'genre': {'genre_name': genre_name, 'description': description}, 'title': 'Thêm Thể loại'})

    return render(request, 'admin_temp/genre/genre_form.html', {'genre': None, 'title': 'Thêm Thể loại'})


# --- 3. Sửa Thể loại (Genre Edit) ---
def genre_edit(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    if request.method == "POST":
        genre.genre_name = request.POST.get('genre_name')
        genre.description = request.POST.get('description')
        genre.save()
        messages.success(request, f"Đã cập nhật thể loại '{genre.genre_name}' thành công.")
        return redirect('genre_list')

    return render(request, 'admin_temp/genre/genre_edit.html',
                  {'genre': genre, 'title': f'Sửa Thể loại: {genre.genre_name}'})


# --- 4. Xóa Thể loại (Single Delete) ---
def genre_delete(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    if request.method == 'POST':
        try:
            genre.delete()
            messages.success(request, f"Thể loại '{genre.genre_name}' đã được xóa thành công.")
        except ProtectedError:
            messages.error(request, f"Không thể xóa thể loại '{genre.genre_name}' do có sản phẩm đang tham chiếu.")
        except Exception as e:
            messages.error(request, f"Đã xảy ra lỗi: {e}")

        return redirect('genre_list')

    # GET request → render template xác nhận xóa
    return render(request, 'admin_temp/genre/genre_delete.html', {'genre': genre})


# --- 5. Chi tiết Thể loại (Genre Detail) ---
def genre_detail(request, pk):
    genre = get_object_or_404(Genre, pk=pk)

    # Lấy sản phẩm thông qua bảng trung gian
    product_ids = Genre_Item.objects.filter(genre=genre).values_list('product_id', flat=True)
    products = Product.objects.filter(id__in=product_ids)

    context = {
        'genre': genre,
        'products': products,
    }
    return render(request, 'admin_temp/genre/genre_detail.html', context)


# --- 6. Xóa nhiều Thể loại (Bulk Delete) ---
def genre_bulk_delete(request):
    if request.method == 'POST':
        genre_ids = request.POST.getlist('genre_ids')

        if genre_ids:
            try:
                deleted_count, _ = Genre.objects.filter(id__in=genre_ids).delete()
                messages.success(request, f"Đã xóa thành công {deleted_count} thể loại.")
            except ProtectedError:
                messages.error(request, "Không thể xóa một số thể loại do chúng đang được sử dụng bởi các sản phẩm.")
            except Exception as e:
                messages.error(request, f"Đã xảy ra lỗi khi xóa hàng loạt: {e}")

        return redirect('genre_list')

    return redirect('genre_list')