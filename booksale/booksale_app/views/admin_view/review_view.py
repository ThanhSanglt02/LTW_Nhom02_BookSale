from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from ...models import Review  # No ReplyReview import needed


@login_required
def review_list(request):
    qs = Review.objects.select_related("product", "creator").order_by("-date_created")

    # --- Lọc theo số sao ---
    rating = request.GET.get("rating")
    if rating:
        qs = qs.filter(rating=rating)

    # --- Lọc theo tên khách hàng ---
    search = request.GET.get("search", "").strip()
    if search:
        qs = qs.filter(creator__username__icontains=search)

    # --- Phân trang ---
    paginator = Paginator(qs, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "admin_temp/review/review_list.html", {
        "page_obj": page_obj,
        "reviews": page_obj.object_list,
        "current_rating": rating,
        "current_search": search,
    })


@login_required
def reply_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if request.method == "POST":
        message = request.POST.get("message", "").strip()
        if not message:
            messages.error(request, "Nội dung trả lời không được để trống.")
            return redirect("reply_review", review_id=review.id)

        # Save reply directly on Review model
        review.reply_message = message
        review.reply_staff = request.user
        review.save()

        return redirect("review_list")

    # Truyền existing_reply vào template
    existing_reply = type("Obj", (), {"message": review.reply_message})() if review.reply_message else None

    return render(request, "admin_temp/review/reply_review.html", {
        "review": review,
        "existing_reply": existing_reply
    })