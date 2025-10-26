from django.shortcuts import render

# Create your views here.

def adm_order_list(request):
    return render(request, 'admin_temp/order/order_list.html')

# class HomeView(View):
#     def get(self, request):
#         return render(request, 'home.html')