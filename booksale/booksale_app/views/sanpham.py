from django.shortcuts import render

def product_list(request):
    products = [
        {
            'id': 'SP001',
            'name': 'Sách Quản trị học chương 1-4',
            'category': 'Sách giáo trình',
            'image': 'images/img.png',
            'quantity': 50,
            'price': 75000,
        }
    ] * 7
    return render(request, 'Product/product_list.html', {'products': products})
