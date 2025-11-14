#giohang.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from booksale_app.models import Cart, Cart_Item, Customer

@login_required
def cart(request):
    
    if not request.user.is_authenticated:
        return render(request, 'user_temp/cart/cart.html', {
            'giohang': [],
            'tong_cong': 0
        })
    
    # Lấy hoặc tạo Customer từ User (auth_user)
    # QUAN TRỌNG: Đảm bảo chỉ lấy Customer của user hiện tại
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
    # QUAN TRỌNG: Chỉ lấy Cart của customer hiện tại
    # Đảm bảo filter theo customer
    cart, created = Cart.objects.get_or_create(customer=customer)
    
    # Lấy tất cả Cart_Item của cart này (đã filter theo cart của customer hiện tại)
    cart_items = Cart_Item.objects.filter(cart=cart).select_related('product')
    
    # Debug: In ra từng item để kiểm tra
    
    # Format dữ liệu để truyền vào template
    giohang = []
    tong_cong = 0
    
    for item in cart_items:
        # Tính tổng tiền cho từng item
        item_total = float(item.unit_price) * item.quantity
        tong_cong += item_total
        
        # Lấy tên file ảnh
        image_name = 'image.jpg'  # default
        if item.product.image:
            # Lấy tên file từ đường dẫn
            image_path = str(item.product.image)
            if '/' in image_path:
                image_name = image_path.split('/')[-1]
            else:
                image_name = image_path
        
        giohang.append({
            'id': item.id,
            'ten': item.product.product_name,
            'dongia': float(item.unit_price),
            'soluong': item.quantity,
            'hinhanh': image_name,
            'product_id': item.product.id,
            'cart_item_id': item.id
        })
    
    
    return render(request, 'user_temp/cart/cart.html', {
        'giohang': giohang,
        'tong_cong': int(tong_cong)
    })
