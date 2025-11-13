from django.db.models import Sum
from booksale_app.models import Category, Cart, Cart_Item, Customer

def categories_and_cart(request):
    """
    Context processor để thêm categories và số lượng giỏ hàng vào tất cả templates
    """
    context = {
        'categories': Category.objects.all()[:3],  # Lấy 3 categories đầu tiên cho menu
        'cart_count': 0
    }
    
    # Đếm số lượng sản phẩm trong giỏ hàng nếu user đã đăng nhập
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(user=request.user)
            cart = Cart.objects.filter(customer=customer).first()
            if cart:
                cart_count = Cart_Item.objects.filter(cart=cart).aggregate(
                    total=Sum('quantity')
                )['total'] or 0
                context['cart_count'] = int(cart_count) if cart_count else 0
        except (Customer.DoesNotExist, AttributeError):
            context['cart_count'] = 0
    
    return context

