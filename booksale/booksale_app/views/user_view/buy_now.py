from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from booksale_app.models import Product, Cart, Cart_Item, Customer
from ..authen_view import group_required

@login_required(login_url="/accounts/login/kh/")
@group_required('KH', login_url="/accounts/login/kh/")
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Lấy hoặc tạo Customer
    customer, created = Customer.objects.get_or_create(
        user=request.user,
        defaults={
            'cust_name': request.user.get_full_name() or request.user.username,
            'email': request.user.email or '',
            'phone': '',
            'address': '',
            'dob': timezone.now().date()
        }
    )

    # Lấy hoặc tạo giỏ hàng
    cart, created = Cart.objects.get_or_create(customer=customer)

    # Thêm sản phẩm
    cart_item, created = Cart_Item.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1, 'unit_price': product.sell_price}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.info(request, f'Đã cập nhật số lượng "{product.product_name}" trong giỏ hàng!')
    else:
        messages.success(request, f'Đã thêm "{product.product_name}" vào giỏ hàng!')

    # Chuyển sang trang cart
    return redirect("cart")


# =============================
# TRANG ORDER
# =============================
@login_required(login_url="/accounts/login/kh/")
@group_required('KH', login_url="/accounts/login/kh/")
def order_page(request):
    customer = Customer.objects.get(user=request.user)
    cart = Cart.objects.get(customer=customer)
    cart_items = Cart_Item.objects.filter(cart=cart)

    return render(request, "user_temp/order/order.html", {
        "cart": cart,
        "cart_items": cart_items,
    })
