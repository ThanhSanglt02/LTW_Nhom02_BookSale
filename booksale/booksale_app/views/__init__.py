# Import các hàm view từ home.py
from .user_view.home import index as home_view
from .admin_view.sanpham import product_list
from .admin_view.chitietsanpham import product_detail
from .authen_view import register_view, login_view, logout_view
from .admin_view.order_view import order_list, order_detail, order_cancel_status, order_confirm_status
from .user_view.category import category_view
from .user_view.category import category_detail_view
from .user_view.category import product_detail_user
from .user_view.add_to_cart import add_to_cart
from .user_view.giohang import giohang
from .user_view.thanhtoan import thanhtoan
from .user_view.donhang import donhang
# Import các hàm view từ product.py
# from .product import index as product_index, detail as product_detail