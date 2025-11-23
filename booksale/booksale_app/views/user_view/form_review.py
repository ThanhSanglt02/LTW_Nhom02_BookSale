from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from ...models import Order, Review

def review_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = order.order_item_set.all()

    # Lọc trùng tên sách
    unique_products = {}
    for item in items:
        key = item.product.product_name.strip().lower()
        if key not in unique_products:
            unique_products[key] = item
    products = list(unique_products.values())

    errors = {}  # lưu sản phẩm thiếu rating/content

    if request.method == "POST":
        for i, product in enumerate(products, start=1):
            content = request.POST.get(f"content_{i}", "").strip()
            rating = request.POST.get(f"rating_{i}", "").strip()
            image = request.FILES.get(f"image_{i}")

            if not content or not rating:
                errors[i] = True  # đánh dấu lỗi
            else:
                Review.objects.create(
                    product_id=product.product.id,
                    content=content,
                    rating=rating,
                    image=image,
                    creator=request.user,
                    date_edited=timezone.now()
                )

        if not errors:
            messages.success(request, "Bạn đã đánh giá sản phẩm thành công!")
            # tất cả hợp lệ → redirect về sản phẩm đầu tiên
            return redirect("product_detail_user", pk=products[0].product.id)

    return render(request, "user_temp/product/review.html", {
        "products": products,
        "errors": errors
    })
