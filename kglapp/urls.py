from django.urls import path
from kglapp import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from . import views
from django.urls import path
from . import views




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
        

]