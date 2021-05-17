from django.contrib.auth.urls import path
from store import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.registration, name='register'),
    path('login/', views.loginuser, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('admin_page/', views.adminpage, name='admin_page'),
    path('user/', views.userpage, name='user'),
    path('add_user/', views.add_new_user, name='add_user'),
    path('user_profile/', views.userprofile, name='user_profile'),
    path('myuser/', views.myusers, name='myuser'),
    path('add_stock/', views.add_new_inventory, name='add_stock'),
    path('buy_stock/', views.buy_inventory, name='buy_stock'),
    path('sell_stock/', views.sell_inventory, name='sell_stock'),
    #     path('get_product_price/', views.get_product_price,
    #          name='get_product_price'),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(
             template_name="password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name="password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_confirm/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="password_reset_done.html"),
         name="password_reset_complete"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
