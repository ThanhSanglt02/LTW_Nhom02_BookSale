from django.shortcuts import render
from booksale_app.models import Product

def search_view(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.filter(product_name__icontains=query) if query else []

    context = {
        'query': query,
        'products': products,
    }
    return render(request, 'user_temp/product/search_result.html', context)
