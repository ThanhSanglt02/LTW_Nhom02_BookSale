from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from booksale_app.models import Order, Order_Item, Customer
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
    elif status_filter == 'cancelled':
        orders = orders.filter(status='cancelled')
    # 'all' thì không filter
    
    # Format dữ liệu để truyền vào template
    order_list = []
    for order in orders:
        order_items = Order_Item.objects.filter(order=order).select_related('product')
        
        # Tính tổng tiền
        total = float(order.total_amount)
        
        # Lấy sản phẩm đầu tiên để hiển thị
        first_item = order_items.first()
        image_name = 'image.jpg'
        if first_item and first_item.product.image:
            image_path = str(first_item.product.image)
            if '/' in image_path:
                image_name = image_path.split('/')[-1]
            else:
                image_name = image_path
        
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
            'image': image_name,
            'product_display': product_display,
            'item_count': order_items.count(),
            'first_item': first_item,
            'name': order_customer.cust_name,
            'phone': order_customer.phone or 'Chưa cập nhật',
            'address': order_customer.address or 'Chưa cập nhật'
        })
    
    # Đếm số lượng đơn hàng theo từng trạng thái
    all_count = Order.objects.filter(customer=customer).count()
    pending_count = Order.objects.filter(customer=customer, status='pending').count()
    confirmed_count = Order.objects.filter(customer=customer, status='confirmed').count()
    cancelled_count = Order.objects.filter(customer=customer, status='cancelled').count()
    
    context = {
        'order_list': order_list,
        'status_filter': status_filter,
        'all_count': all_count,
        'pending_count': pending_count,
        'confirmed_count': confirmed_count,
        'cancelled_count': cancelled_count,
        'customer': customer
    }
    
    return render(request, 'user_temp/my_orders/my_orders.html', context)

