from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from booksale_app.models import Order, Order_Item, Customer, Cart, Cart_Item
from django.db.models import Q
from ..authen_view import group_required

@login_required(login_url="/accounts/login/kh/")
@group_required('KH', login_url="/accounts/login/kh/") 
def my_orders(request):
    """Hiển thị danh sách đơn hàng của user với sidebar"""
    # Lấy hoặc tạo customer của user hiện tại
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
    
    # Lấy filter từ query parameter
    status_filter = request.GET.get('status', 'all')
    
    # Lấy tất cả orders của customer
    orders = Order.objects.filter(customer=customer).order_by('-order_date')
    
    # Filter theo trạng thái
    if status_filter == 'pending':
        orders = orders.filter(status='pending')
    elif status_filter == 'confirmed':
        orders = orders.filter(status='confirmed')
    elif status_filter == 'completed':
        orders = orders.filter(status='completed')
    elif status_filter == 'cancelled':
        orders = orders.filter(status='cancelled')
    # 'all' thì không filter
    
    # Format dữ liệu để truyền vào template
    order_list = []
    for order in orders:
        order_items = Order_Item.objects.filter(order=order).select_related('product')
        
        # Tính tổng tiền
        total = order.total_amount
        
        # Lấy sản phẩm đầu tiên để hiển thị
        first_item = order_items.first()
        first_product = first_item.product if first_item else None
        
        # Tạo tên sản phẩm (nếu có nhiều sản phẩm thì hiển thị "và X sản phẩm khác")
        product_names = [item.product.product_name for item in order_items[:1]]
        if order_items.count() > 1:
            product_display = f"{product_names[0]} và {order_items.count() - 1} sản phẩm khác"
        else:
            product_display = product_names[0] if product_names else "Sản phẩm"
        
        # Lấy thông tin customer từ order
        order_customer = order.customer
        
        order_list.append({
            'order': order,
            'total': total,
            'first_product': first_product,  # Truyền product object để dùng image.url
            'product_display': product_display,
            'item_count': order_items.count(),
            'first_item': first_item,
            'name': order_customer.cust_name,
            'phone': order_customer.phone or 'Chưa cập nhật',
            'address': order_customer.address or 'Chưa cập nhật',
        })
    
    # Đếm số lượng đơn hàng theo từng trạng thái
    all_count = Order.objects.filter(customer=customer).count()
    pending_count = Order.objects.filter(customer=customer, status='pending').count()
    confirmed_count = Order.objects.filter(customer=customer, status='confirmed').count()
    completed_count = Order.objects.filter(customer=customer, status='completed').count()
    cancelled_count = Order.objects.filter(customer=customer, status='cancelled').count()
    
    context = {
        'order_list': order_list,
        'status_filter': status_filter,
        'all_count': all_count,
        'pending_count': pending_count,
        'confirmed_count': confirmed_count,
        'completed_count': completed_count,
        'cancelled_count': cancelled_count,
        'customer': customer
    }
    
    return render(request, 'user_temp/my_orders/my_orders.html', context)


@login_required(login_url="/accounts/login/kh/")
@group_required('KH', login_url="/accounts/login/kh/")
def buy_again(request, order_id):
    """Mua lại: Thêm tất cả sản phẩm từ order vào giỏ hàng"""
    # Lấy customer của user hiện tại
    customer = get_object_or_404(Customer, user=request.user)
    
    # Lấy order và kiểm tra quyền truy cập (chỉ customer của order mới được mua lại)
    order = get_object_or_404(Order, id=order_id, customer=customer)
    
    # Lấy tất cả order items
    order_items = Order_Item.objects.filter(order=order).select_related('product')
    
    if not order_items.exists():
        messages.warning(request, 'Đơn hàng này không có sản phẩm nào!')
        return redirect('my_orders')
    
    # Lấy hoặc tạo Cart cho Customer
    cart, cart_created = Cart.objects.get_or_create(customer=customer)
    
    # Danh sách lỗi và thành công
    errors = []
    success_count = 0
    
    # Duyệt qua từng order item và thêm vào cart
    for order_item in order_items:
        product = order_item.product
        requested_quantity = order_item.quantity
        
        # Kiểm tra số lượng sản phẩm còn lại
        if product.quantity < requested_quantity:
            errors.append(
                f'Sản phẩm "{product.product_name}" chỉ còn {product.quantity} sản phẩm. '
                f'Bạn muốn mua lại {requested_quantity} sản phẩm.'
            )
            continue
        
        # Kiểm tra xem sản phẩm đã có trong cart chưa
        cart_item, item_created = Cart_Item.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={
                'quantity': requested_quantity,
                'unit_price': product.sell_price  # Sử dụng giá hiện tại
            }
        )
        
        # Nếu sản phẩm đã có trong cart, cộng thêm số lượng
        if not item_created:
            # Kiểm tra tổng số lượng sau khi cộng
            new_quantity = cart_item.quantity + requested_quantity
            if new_quantity > product.quantity:
                errors.append(
                    f'Sản phẩm "{product.product_name}" chỉ còn {product.quantity} sản phẩm. '
                    f'Trong giỏ hàng đã có {cart_item.quantity} sản phẩm, bạn muốn thêm {requested_quantity} sản phẩm.'
                )
                continue
            
            cart_item.quantity = new_quantity
            cart_item.unit_price = product.sell_price  # Cập nhật giá mới nhất
            cart_item.save()
        else:
            success_count += 1
    
    # Cập nhật updated_at của cart
    cart.updated_at = timezone.now()
    cart.save()
    
    # Hiển thị thông báo
    if errors:
        for error in errors:
            messages.error(request, error)
    
    if success_count > 0:
        if success_count == order_items.count():
            messages.success(request, f'Đã thêm tất cả {success_count} sản phẩm vào giỏ hàng!')
        else:
            messages.warning(request, f'Đã thêm {success_count} sản phẩm vào giỏ hàng. Một số sản phẩm không đủ số lượng.')
    
    # Nếu có lỗi, quay lại trang my_orders, nếu không thì chuyển sang cart
    if errors and success_count == 0:
        return redirect('my_orders')
    else:
        return redirect('cart')

