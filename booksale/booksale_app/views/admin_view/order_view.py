from django.shortcuts import render, get_object_or_404
from booksale_app.models import Order, Customer
# Create your views here.

def adm_order_list(request):
    orders =  Order.objects.select_related('customer').order_by('-order_date') # select_related('customer') để lấy luôn thông tin khách hàng
    
    context = {
        'orders': orders
    }

    return render(request, 'admin_temp/order/order_list.html', context)

def order_detail(request, pk):
    order = get_object_or_404(Order, pk = pk)  # get_object_ỏr_404 dùng để lấy đối tượng cụ thể chứ không thế lấy danh sách --> nếu lấy ds thì phải model.objects.all()
    order_info = {'order': order}

    return render(request, 'admin_temp/order/order_detail.html', order_info)
# def edit_order(request, pk = None):
#     if pk is not None:
#         publisher = get_object_or_404(Order, pk = pk)
#     else:
#         publisher = None

#     if request.method == 'POST':
#         form = PublisherForm(request.POST, instance=publisher)
#         if form.is_valid():
#             # luwu object vào db
#             # updated_publisher chứa thông tin mà cái Model Publisher nó return ở hàm __str__
#             updated_publisher = form.save()
#             if publisher is None:
#                 messages.success(request, "Publisher {} was created.".format(updated_publisher))
#             else: 
#                 messages.success(request, "Publisher {} was updated.".format(updated_publisher))
#             # mở lại trang publisher_edit với ID của publisher đã lưu. --> ban đầu chưa có pk thì sẽ đi vào đường dẫn publishers/new. Sau khi taoj mới sucess thì đường dẫn sẽ được cập nhật kèm theo pk thay vì None
#                     # và lúc này pk đã có nên nó sẽ lấy url publishers/<int:pk>/
#             return redirect("publisher_edit", updated_publisher.pk) #pk tương ứng với cột id trong db
#     else:
#         form = PublisherForm(instance=publisher)
#     return render(request, "form_example.html", {"method": request.method, "form": form})

# class HomeView(View):
#     def get(self, request):
#         return render(request, 'home.html')