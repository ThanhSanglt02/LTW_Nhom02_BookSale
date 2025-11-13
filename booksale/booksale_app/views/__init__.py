# Import các hàm view từ home.py
from .user_view.home import home_view
from .admin_view.sanpham import product_list
from .admin_view.chitietsanpham import product_detail
from .authen_view import register_view, login_view, logout_view, role_redirect_view, order_list
from .admin_view.order_view import order_detail, order_cancel_status, order_confirm_status
from .user_view.category import category_view, category_detail_view, product_detail_user
from .user_view.add_to_cart import add_to_cart
from .user_view.cart import cart
from .user_view.order import order
from .user_view.donhang import donhang
