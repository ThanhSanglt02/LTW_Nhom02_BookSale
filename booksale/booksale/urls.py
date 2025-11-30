"""
URL configuration for booksale project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin, auth
from django.urls import path, include
from booksale_app import views
from django.conf import settings
# from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('booksale_app.urls')),

    path("accounts/",include(("django.contrib.auth.urls", "auth"),namespace="accounts")),

    # Password reset
    path("accounts/password_reset/done/",auth.views.PasswordResetDoneView.as_view(),name="password_reset_done",),
    path("accounts/reset/done/",auth.views.PasswordResetCompleteView.as_view(),name="password_reset_complete",),

    # Role redirect sau login
    path("accounts/role_redirect/", views.role_redirect_view, name="role_redirect"),
    
    ## REGISTER URL
    path('accounts/register/', views.register_view, name = 'register'),

    ## LOGIN URLS
    # Login KH
    path("accounts/login/kh/", 
         views.RoleLoginView.as_view(
             extra_context={"required_group": "KH"}
         ),
         name="login_kh"),
    # Login Nhân viên Bán hàng
    path("accounts/login/staff/", 
         views.RoleLoginView.as_view(
             extra_context={"required_group": ["NVBH", "NVTK"]}
         ),
         name="login_staff"),
    
    # LOGOUT URLS
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
