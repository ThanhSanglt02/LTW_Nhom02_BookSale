from django.shortcuts import render

def product_detail(request):
    # Dữ liệu mẫu để hiển thị lên giao diện
    product = {
        'name': 'Đắc Nhân Tâm',
        'author': 'Dale Carnegie',
        'price': '90.000 VND',
        'description': 'Cuốn sách kinh điển giúp người đọc thấu hiểu nghệ thuật giao tiếp và đối nhân xử thế.'
    }

    related_products = [
        {'name': 'Nghệ thuật nói chuyện', 'price': '85.000 VND'},
        {'name': 'Quẳng gánh lo đi mà vui sống', 'price': '88.000 VND'},
        {'name': 'Đắc Nhân Tâm (bản đầy đủ)', 'price': '95.000 VND'},
    ]

    return render(request, 'dathang/product_detail.html', {
        'product': product,
        'related_products': related_products
    })
