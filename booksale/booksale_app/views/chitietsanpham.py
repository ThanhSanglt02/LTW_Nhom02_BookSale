from django.shortcuts import render

def product_detail(request):
    return render(request, 'product_detail.html')
