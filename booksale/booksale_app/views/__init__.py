# Import các hàm view từ home.py
from .user_view.home import home_view
# Import các hàm view từ product.py
# from .product import index as product_index, detail as product_detail
from .admin_view.chitietsanpham import product_detail
from .authen_view import role_redirect_view, register_view, RoleLoginView, CustomLogoutView
from .admin_view.order_view import order_detail, order_cancel_status, order_confirm_status, order_list
from .user_view.add_to_cart import add_to_cart
from .admin_view.sanpham import product_list
from .admin_view.chitietsanpham import product_detail
from .user_view.category import category_view, category_detail_view, product_detail_user
from .user_view.add_to_cart import add_to_cart
from .user_view.cart import cart
from .user_view.order import order
from .user_view.donhang import donhang
from .user_view.buy_now import buy_now
from .user_view.search import search_view
from .user_view.review import submit_review
from .user_view.form_review import submit_review1

