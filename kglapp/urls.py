from django.urls import path
from kglapp import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from . import views
from django.urls import path
from . import views
from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
        path('login/',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
        path('',views.index,name='index'),
        path('home/',views.home,name='home'),
        path('procurement/',views.add_procurement,name='procurement'),
        path('logout/', LogoutView.as_view(), name='logout'),
        path('record-sale/', views.record_sale, name='record_sale'),
        path('sale-success/', views.sale_success, name='sale_success'),
        path('sales-list/', views.sales_list, name='sales_list'),
        path('record-credit/', views.record_credit_sale, name='record_credit_sale'),
        path('credit-sales/', views.credit_sales_list, name='credit_sales_list'),
        path('daily-sales/', views.daily_sales_report, name='daily_sales'),
        path('stock/', views.stock_page, name='stock_page'),
        path('signup/', views.signup_view, name='signup'),
        path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
        path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="reset_password_sent.html"), name='password_reset_done'),
        path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="reset_password_confirm.html"), name='password_reset_confirm'),
        path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="reset_password_complete.html"), name='password_reset_complete'),
      

]

        

