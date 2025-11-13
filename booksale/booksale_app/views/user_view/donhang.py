from django.shortcuts import render
from django.templatetags.static import static

def donhang(request):
    # Dữ liệu sản phẩm mẫu
    product = {
        'id': 1,
        'ten': 'Sách quản trị học',
        'tacgia': 'Phích windowToylar',
        'namxuatban': '2017',
        'nhaxuatban': 'NXB Đại Học Quốc Gia Hà Nội',
        'dongia': 15000,
        'soluong': 1,
        'hinhanh': 'image.jpg'
    }

    tam_tinh = product['dongia'] * product['soluong']
    phi_van_chuyen = 0
    tong_cong = tam_tinh + phi_van_chuyen

    context = {
        'product': product,
        'tam_tinh': tam_tinh,
        'phi_van_chuyen': phi_van_chuyen,
        'tong_cong': tong_cong
    }

    return render(request, 'user_temp/donhang/donhang.html', context)