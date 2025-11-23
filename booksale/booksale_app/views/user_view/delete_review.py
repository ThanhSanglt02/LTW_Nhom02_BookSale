from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from ...models import Review

def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if review.creator != request.user:
        messages.error(request, "Bạn không có quyền xóa đánh giá này.")
        return redirect('product_detail_user', review.product.id)

    if request.method == "POST":
        review.delete()
        messages.success(request, "Đã xóa đánh giá thành công.")
        return redirect('product_detail_user', review.product.id)

    return redirect('product_detail_user', review.product.id)
