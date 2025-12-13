from django.shortcuts import render, get_object_or_404
from ...models import Category, Product, Review  # Import các model cần dùng: Category, Product, Review

# --------------------------------------
# HIỂN THỊ TẤT CẢ DANH MỤC SẢN PHẨM
# --------------------------------------
def category_view(request): #chứa thông tin của người dùng gửi lên (GET, POST, session…).
    categories = Category.objects.all()  # Lấy toàn bộ category trong database
    return render(request, 'user_temp/product/category.html', {
        'categories': categories  # Truyền dữ liệu categories sang template html
    })

# --------------------------------------
# HIỂN THỊ CHI TIẾT 1 DANH MỤC = DANH SÁCH SẢN PHẨM TRONG CATEGORY
# --------------------------------------
def category_detail_view(request, category_name):#chứa dữ liệu gửi từ trình duyệt, được lấy từ URL
    category = Category.objects.get(category_name=category_name)
    # Tìm category dựa vào tên category truyền từ URL
    products = category.product_set.all()
    # Lấy tất cả sản phẩm thuộc category này (Django tự tạo product_set)

    return render(request, 'user_temp/product/category_detail.html', {
        'category': category,    # Truyền thông tin category
        'products': products     # Truyền danh sách sản phẩm trong category này
    })

# --------------------------------------
# TRANG CHI TIẾT SẢN PHẨM
# --------------------------------------
def product_detail_user(request, pk):
    product = get_object_or_404(Product, pk=pk)
    # Lấy sản phẩm theo pk, không có thì trả về 404 tránh crash

    # -------------------------------
    # LỌC REVIEW THEO SỐ SAO
    # -------------------------------
    rating = request.GET.get("rating")
    # Lấy số sao từ ?rating=5 trong URL (nếu có)

    # Lấy tất cả review của sản phẩm, sắp xếp mới nhất trước
    reviews = Review.objects.filter(product=product).order_by('-date_created')

    if rating:
        # Nếu người dùng chọn số sao (ví dụ rating=5) → lọc review theo đúng số sao
        reviews = reviews.filter(rating=rating)

    # -------------------------------
    # SẢN PHẨM LIÊN QUAN
    # -------------------------------
    related_products = Product.objects.filter(
        category=product.category   # Trùng category với sản phẩm đang xem
    ).exclude(pk=pk)[:4]            # Không lấy chính nó + giới hạn 4 sản phẩm

    # -------------------------------
    # TRẢ DỮ LIỆU CHO TEMPLATE
    # -------------------------------
    return render(request, 'user_temp/product/product_detail.html', {
        'product': product,                 # Thông tin sản phẩm
        'related_products': related_products,  # Danh sách sản phẩm liên quan
        'reviews': reviews,                 # Danh sách review (đã áp dụng lọc nếu có)
    })