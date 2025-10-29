from django.shortcuts import render

def product_detail(request):
    return render(request, 'admin_temp/product/product_detail.html')
