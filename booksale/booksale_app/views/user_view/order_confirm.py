from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from booksale_app.models import Order, Order_Item, Customer, Product
from ..authen_view import group_required

@login_required(login_url="/accounts/login/kh/")
@group_required('KH', login_url="/accounts/login/kh/") 
def order_confirm(request, order_id):
    """Hiển thị thông tin xác nhận đơn hàng"""
    # Lấy customer của user hiện tại
    customer = get_object_or_404(Customer, user=request.user)
    
    # Lấy order và kiểm tra quyền truy cập (chỉ customer của order mới xem được)
    order = get_object_or_404(Order, id=order_id, customer=customer)
    
    # Lấy tất cả order items
    order_items = Order_Item.objects.filter(order=order).select_related('product')
    
    # Format dữ liệu để truyền vào template
    products = []
    tam_tinh = 0
    
    for item in order_items:
        item_total = item.total_price
        tam_tinh += item_total
        
        # Lấy tên file ảnh
        image_name = 'image.jpg'  # default
        if item.product.image:
            image_path = str(item.product.image)
            if '/' in image_path:
                image_name = image_path.split('/')[-1]
            else:
                image_name = image_path
        
        products.append({
            'id': item.id,
            'ten': item.product.product_name,
            'dongia': item.unit_price,
            'soluong': item.quantity,
            'tong': item_total,
            'hinhanh': image_name,
            'product': item.product
        })
    
    phi_van_chuyen = 0
    tong_cong = tam_tinh + phi_van_chuyen
    
    context = {
        'order': order,
        'products': products,
        'customer': customer,
        'tam_tinh': tam_tinh,
        'phi_van_chuyen': phi_van_chuyen,
        'tong_cong': tong_cong
    }

    return render(request, 'user_temp/order_confirm/order_confirm.html', context)

@login_required(login_url="/accounts/login/kh/")
@group_required('KH', login_url="/accounts/login/kh/") 
@require_POST
def cancel_order(request, order_id):
    """Hủy đơn hàng - chỉ cho phép khi trạng thái là pending"""
    # Lấy customer của user hiện tại
    customer = get_object_or_404(Customer, user=request.user)
    
    # Lấy order và kiểm tra quyền truy cập (chỉ customer của order mới hủy được)
    order = get_object_or_404(Order, id=order_id, customer=customer)
    
    # Chỉ cho phép hủy khi trạng thái là pending
    if order.status != 'pending':
        messages.error(request, 'Chỉ có thể hủy đơn hàng khi đang ở trạng thái "Chờ xác nhận"!')
        return redirect('order_confirm', order_id=order_id)
    
    # Lấy lý do hủy (nếu có)
    cancel_reason = request.POST.get('cancel_reason', 'Khách hàng yêu cầu hủy đơn hàng')
    
    # Cập nhật trạng thái đơn hàng
    order.status = 'cancelled'
    order.cancel_reason = cancel_reason
    order.save()
    
    # Hoàn trả số lượng sản phẩm về kho
    order_items = Order_Item.objects.filter(order=order).select_related('product')
    for item in order_items:
        product = item.product
        product.quantity += item.quantity
        product.save()
    
    messages.success(request, 'Đã hủy đơn hàng thành công!')
    return redirect('order_confirm', order_id=order_id)