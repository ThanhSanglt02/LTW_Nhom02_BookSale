# booksale_app/views/user_view/form_review.py
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from ...models import Review, Product
from django.contrib import messages

def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, creator=request.user)
    product = review.product

    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        rating = request.POST.get("rating", "").strip()
        image = request.FILES.get("image")

        if not content or not rating:
            messages.error(request, "Vui lòng nhập đủ nội dung và đánh giá.")
        else:
            review.content = content
            review.rating = rating
            if image:
                review.image = image
            review.date_edited = timezone.now()
            review.save()
            messages.success(request, "Cập nhật đánh giá thành công!")
            return redirect("product_detail_user", pk=product.id)

    return render(request, "user_temp/product/edit_review.html", {
        "review": review,
        "product": product
    })
