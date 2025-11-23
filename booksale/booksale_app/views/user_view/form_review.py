from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from ...models import Product, Review


@login_required
def submit_review1(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        content = request.POST.get("content")
        rating = request.POST.get("rating")
        image = request.FILES.get("image")

        Review.objects.create(
            content=content,
            rating=rating,
            image=image,
            creator=request.user,
            product=product,
            date_edited=timezone.now()
        )

        return redirect('product_detail_user', pk=product_id)

    return render(request, "user_temp/product/submit_review.html", {"product": product})
