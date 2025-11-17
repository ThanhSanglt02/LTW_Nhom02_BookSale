#giohang.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..authen_view import group_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from booksale_app.models import Cart, Cart_Item, Customer, Product

@login_required(login_url="/accounts/login/kh/")
@group_required('KH', login_url="/accounts/login/kh/") 
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
            'tong': item_total,  # Tổng tiền = đơn giá * số lượng
            'hinhanh': image_name,
            'product_id': item.product.id,
            'cart_item_id': item.id,
            'max_quantity': item.product.quantity  # Số lượng tối đa có sẵn
        })
    
    
    return render(request, 'user_temp/cart/cart.html', {
        'giohang': giohang,
        'tong_cong': int(tong_cong), 
        
    })


@login_required(login_url="/accounts/login/kh/")
@group_required('KH', login_url="/accounts/login/kh/") 
@require_POST
def delete_cart_items(request):
    """Xóa các item trong giỏ hàng"""
    # Lấy customer của user hiện tại
    customer = get_object_or_404(Customer, user=request.user)
    cart = get_object_or_404(Cart, customer=customer)
    
    # Lấy các item IDs từ request
    item_id = request.POST.get('item_id')  # Xóa một item (dấu X)
    selected_items = request.POST.getlist('selected_items[]')  # Xóa nhiều item (checkbox)
    delete_all = request.POST.get('delete_all') == 'true'  # Xóa tất cả
    
    try:
        if item_id:
            # Xóa một item cụ thể
            cart_item = get_object_or_404(Cart_Item, id=item_id, cart=cart)
            cart_item.delete()
            return JsonResponse({'success': True, 'message': 'Đã xóa sản phẩm khỏi giỏ hàng'})
        
        elif delete_all:
            # Xóa tất cả items trong cart
            Cart_Item.objects.filter(cart=cart).delete()
            return JsonResponse({'success': True, 'message': 'Đã xóa tất cả sản phẩm khỏi giỏ hàng'})
        
        elif selected_items:
            # Xóa các item được chọn
            item_ids = [int(id) for id in selected_items]
            Cart_Item.objects.filter(id__in=item_ids, cart=cart).delete()
            return JsonResponse({'success': True, 'message': f'Đã xóa {len(item_ids)} sản phẩm khỏi giỏ hàng'})
        
        else:
            return JsonResponse({'success': False, 'message': 'Không có item nào được chọn để xóa'})
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Lỗi: {str(e)}'})


@login_required(login_url="/accounts/login/kh/")
@group_required('KH', login_url="/accounts/login/kh/") 
@require_POST
def update_cart_quantities(request):
    """Cập nhật số lượng các sản phẩm trong giỏ hàng và kiểm tra số lượng có sẵn"""
    customer = get_object_or_404(Customer, user=request.user)
    cart = get_object_or_404(Cart, customer=customer)
    
    # Lấy dữ liệu số lượng từ request
    # Format: quantities[] = [{'item_id': 1, 'quantity': 2}, ...]
    errors = []
    updated_items = []
    
    try:
        # Lấy tất cả cart items
        cart_items = Cart_Item.objects.filter(cart=cart).select_related('product')
        
        for cart_item in cart_items:
            item_id = str(cart_item.id)
            new_quantity = request.POST.get(f'quantity_{item_id}')
            
            if new_quantity:
                try:
                    new_qty = int(new_quantity)
                    if new_qty < 0:
                        errors.append(f'Số lượng "{cart_item.product.product_name}" không hợp lệ')
                        continue
                    
                    # Kiểm tra số lượng sản phẩm có sẵn
                    if new_qty > cart_item.product.quantity:
                        errors.append(
                            f'Sản phẩm "{cart_item.product.product_name}" chỉ còn {cart_item.product.quantity} sản phẩm. '
                            f'Bạn đang chọn {new_qty} sản phẩm.'
                        )
                        continue
                    
                    # Cập nhật số lượng
                    cart_item.quantity = new_qty
                    cart_item.save()
                    updated_items.append(cart_item)
                    
                except ValueError:
                    errors.append(f'Số lượng không hợp lệ cho sản phẩm "{cart_item.product.product_name}"')
        
        if errors:
            # Có lỗi, trả về danh sách lỗi
            return JsonResponse({
                'success': False,
                'errors': errors,
                'message': 'Có lỗi xảy ra khi cập nhật giỏ hàng'
            })
        else:
            # Cập nhật thành công
            return JsonResponse({
                'success': True,
                'message': 'Đã cập nhật giỏ hàng thành công'
            })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        })


@login_required(login_url="/accounts/login/kh/")
@group_required('KH', login_url="/accounts/login/kh/") 
@require_POST
def proceed_to_order(request):
    """Xử lý khi click 'Mua hàng': cập nhật số lượng và chuyển sang trang order"""
    customer = get_object_or_404(Customer, user=request.user)
    cart = get_object_or_404(Cart, customer=customer)
    
    # Lấy tất cả cart items
    cart_items = Cart_Item.objects.filter(cart=cart).select_related('product')
    errors = []
    
    # Kiểm tra và cập nhật số lượng từ form
    for cart_item in cart_items:
        item_id = str(cart_item.id)
        new_quantity = request.POST.get(f'quantity_{item_id}')
        
        if new_quantity:
            try:
                new_qty = int(new_quantity)
                if new_qty < 0:
                    errors.append(f'Số lượng "{cart_item.product.product_name}" không hợp lệ')
                    continue
                
                # Kiểm tra số lượng sản phẩm có sẵn
                if new_qty > cart_item.product.quantity:
                    errors.append(
                        f'Sản phẩm "{cart_item.product.product_name}" chỉ còn {cart_item.product.quantity} sản phẩm. '
                        f'Bạn đang chọn {new_qty} sản phẩm.'
                    )
                    continue
                
                # Cập nhật số lượng
                cart_item.quantity = new_qty
                cart_item.save()
                
            except ValueError:
                errors.append(f'Số lượng không hợp lệ cho sản phẩm "{cart_item.product.product_name}"')
    
    # Nếu có lỗi, hiển thị và quay lại trang cart
    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect('cart')
    
    # Không có lỗi, chuyển sang trang order
    return redirect('order')
