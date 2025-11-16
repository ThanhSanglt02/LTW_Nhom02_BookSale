from django.shortcuts import render, redirect, get_object_or_404
from ...models import Product, Review
from django.contrib.auth.decorators import login_required

@login_required
def submit_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        rating = request.POST.get("rating")
        content = request.POST.get("content")
        image = request.FILES.get("image")

        Review.objects.create(
            product=product,
            creator=request.user,
            rating=rating,
            content=content,
            image=image
        )
        return redirect('product_detail_user', pk=product.id)  # pk phải khớp URL

    # Nếu GET, redirect về trang chi tiết sản phẩm
    return redirect('product_detail_user', pk=product.id)
