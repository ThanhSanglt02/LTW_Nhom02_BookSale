#giohang.py
from django.shortcuts import render
from django.templatetags.static import static

def thanhtoan(request):
    # giohang = [
    #     {'id': 1, 'ten': 'Tên sách 1', 'dongia': 20000, 'soluong': 2, 'hinhanh': 'sach1.jpg'},
    #     {'id': 2, 'ten': 'Tên sách 2', 'dongia': 10000, 'soluong': 2, 'hinhanh': 'sach2.jpg'},
    #     {'id': 3, 'ten': 'Tên sách 3', 'dongia': 30000, 'soluong': 2, 'hinhanh': 'sach3.jpg'},
    #     {'id': 4, 'ten': 'Tên sách 4', 'dongia': 40000, 'soluong': 2, 'hinhanh': 'sach4.jpg'},
    # ]

    # tong_cong = sum(item['dongia'] * item['soluong'] for item in giohang)
    return render(
      request, 'user_temp/thanhtoan/thanhtoan.html'
    # {'giohang': giohang, 'tong_cong': tong_cong}
    )