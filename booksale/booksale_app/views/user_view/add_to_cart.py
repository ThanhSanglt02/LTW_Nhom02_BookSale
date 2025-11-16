from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from booksale_app.models import Product, Cart, Cart_Item, Customer
from decimal import Decimal
from ..authen_view import group_required

@login_required(login_url="/accounts/login/kh/")
@group_required('KH', login_url="/accounts/login/kh/")
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Lấy hoặc tạo Customer từ User
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
    
    # Lấy hoặc tạo Cart cho Customer
    cart, cart_created = Cart.objects.get_or_create(customer=customer)
    
    # Lấy hoặc tạo Cart_Item cho sản phẩm trong cart
    cart_item, item_created = Cart_Item.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={
            'quantity': 1,
            'unit_price': product.sell_price
        }
    )
    
    # Nếu sản phẩm đã có trong cart thì tăng số lượng
    if not item_created:
        cart_item.quantity += 1
        cart_item.unit_price = product.sell_price  # Cập nhật giá mới nhất
        cart_item.save()
    
    # Cập nhật updated_at của cart
    cart.updated_at = timezone.now()
    cart.save()
    
    messages.success(request, f'Đã thêm "{product.product_name}" vào giỏ hàng!')
    
    return redirect(request.META.get('HTTP_REFERER', '/'))
