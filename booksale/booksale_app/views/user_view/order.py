#giohang.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from decimal import Decimal
from booksale_app.models import Cart, Cart_Item, Customer, Order, Order_Item, Product
from ..authen_view import group_required

@login_required(login_url="/accounts/login/kh/")
@group_required('KH', login_url="/accounts/login/kh/") 
def order(request):
    """Hiển thị trang đặt hàng với danh sách sản phẩm từ giỏ hàng"""
    # Lấy customer của user hiện tại
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
    
    # Lấy cart của customer
    cart = Cart.objects.filter(customer=customer).first()
    
    if not cart:
        messages.warning(request, 'Giỏ hàng của bạn đang trống!')
        return redirect('cart')
    
    # Lấy tất cả cart items
    cart_items = Cart_Item.objects.filter(cart=cart).select_related('product')
    
    if not cart_items.exists():
        messages.warning(request, 'Giỏ hàng của bạn đang trống!')
        return redirect('cart')
    
    # Format dữ liệu để truyền vào template
    giohang = []
    tong_cong = 0
    
    for item in cart_items:
        item_total = float(item.unit_price) * item.quantity
        tong_cong += item_total
        
        # Lấy tên file ảnh
        image_name = 'image.jpg'  # default
        if item.product.image:
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
            'tong': item_total,
            'hinhanh': image_name,
            'product_id': item.product.id,
            'cart_item_id': item.id,
            'product': item.product  # Truyền product object để dùng trong template
        })
    
    return render(request, 'user_temp/order/order.html', {
        'giohang': giohang,
        'tong_cong': int(tong_cong),
        'customer': customer
    })


@login_required(login_url="/accounts/login/kh/")
@group_required('KH', login_url="/accounts/login/kh/") 
def create_order(request):
    """Xử lý đặt hàng: tạo Order, Order_Item và xóa Cart_Item"""
    if request.method != 'POST':
        return redirect('order')
    
    # Lấy customer của user hiện tại
    customer = get_object_or_404(Customer, user=request.user)
    
    # Lấy cart của customer
    cart = get_object_or_404(Cart, customer=customer)
    cart_items = Cart_Item.objects.filter(cart=cart).select_related('product')
    
    if not cart_items.exists():
        messages.error(request, 'Giỏ hàng của bạn đang trống!')
        return redirect('cart')
    
    # Lấy dữ liệu từ form
    phone = request.POST.get('phone', '').strip()
    email = request.POST.get('email', '').strip()
    address = request.POST.get('address', '').strip()
    note = request.POST.get('note', '').strip()
    payment_method = request.POST.get('payment', 'cash')
    
    # Validate dữ liệu bắt buộc
    if not phone or not address:
        messages.error(request, 'Vui lòng điền đầy đủ thông tin bắt buộc!')
        return redirect('order')
    
    # Cập nhật thông tin customer
    customer.phone = phone
    if email:
        customer.email = email
    customer.address = address
    customer.save()
    
    # Tính tổng tiền
    total_amount = Decimal('0')
    for item in cart_items:
        item_total = Decimal(str(item.unit_price)) * Decimal(str(item.quantity))
        total_amount += item_total
    
    # Kiểm tra số lượng sản phẩm có sẵn
    errors = []
    for item in cart_items:
        if item.quantity > item.product.quantity:
            errors.append(
                f'Sản phẩm "{item.product.product_name}" chỉ còn {item.product.quantity} sản phẩm. '
                f'Bạn đang chọn {item.quantity} sản phẩm.'
            )
    
    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect('order')
    
    try:
        # Tạo Order
        order = Order.objects.create(
            customer=customer,
            total_amount=total_amount,
            payment_method=payment_method,
            status='pending'
        )
        
        # Tạo Order_Item và cập nhật số lượng sản phẩm
        for cart_item in cart_items:
            # Tạo Order_Item
            item_total = Decimal(str(cart_item.unit_price)) * Decimal(str(cart_item.quantity))
            Order_Item.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                total_price=item_total
            )
            
            # Giảm số lượng sản phẩm trong kho
            cart_item.product.quantity -= cart_item.quantity
            cart_item.product.save()
        
        # Xóa tất cả Cart_Item
        cart_items.delete()
        
        messages.success(request, f'Đặt hàng thành công! Mã đơn hàng: #{order.id}')
        return redirect('order_confirm', order_id=order.id)
    
    except Exception as e:
        messages.error(request, f'Có lỗi xảy ra khi đặt hàng: {str(e)}')
        return redirect('order')