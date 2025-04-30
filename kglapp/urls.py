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
from django.shortcuts import render
from django.urls import path
from .views import director_dashboard
from django.urls import path
from .views import add_product
from .views import faq_view  # 👈 Import the view function
from .views import branch_sales_report


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
        path('daily-sales/', views.daily_sales_report, name='daily_sales'),
        path('stock/', views.stock_page, name='stock_page'),
        # path('signup/', views.signup, name='signup'),
        path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
        path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="reset_password_sent.html"), name='password_reset_done'),
        path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="reset_password_confirm.html"), name='password_reset_confirm'),
        path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="reset_password_complete.html"), name='password_reset_complete'),
        path('credits/', views.credit_list, name='credit_list'),
        path('director_dashboard/', views.director_dashboard, name='director_dashboard'),
        path('maganjo-sales/', views.maganjo_sales_report, name='maganjo_sales_report'),
        # path('rules/', views.company_rules, name='company_rules'),
        # path('profile/', views.user_profile, name='user_profile'),
        path('branch-comparison/', views.branch_comparison_dashboard, name='branch_comparison_dashboard'),
        path('credit-recovery-report/', views.credit_recovery_report, name='credit_recovery_report'),
        path('sales-agent-performance/', views.sales_agent_performance, name='sales_agent_performance'),
        path('add-product/', add_product, name='add_product'),
        path('product-list/', views.product_list, name='product_list'),
        path('procurements/', views.procurement_list, name='procurement_list'),
        path('faq/', faq_view, name='faq'),
        path('contact/', views.contact_support, name='contact_support'),
        path('thank-you/', views.thank_you, name='thank_you'),
        path('low-stock-alerts/', views.low_stock_alerts, name='low_stock_alerts'),
        path('suppliers/', views.supplier_list, name='supplier_list'),  # List suppliers
        path('suppliers/add/', views.add_supplier, name='add_supplier'),  # Add supplier
        path('branches/', views.branch_list, name='branch_list'),
        path('branches/add/', views.add_branch, name='add_branch'),
        path('dashboard/sales-agent/matugga/', views.sales_agent_dashboard_matugga, name='sales_agent_dashboard_matugga'),
        path('dashboard/sales-agent/maganjo/', views.sales_agent_dashboard_maganjo, name='sales_agent_dashboard_maganjo'),
        path('sale/<int:pk>/', views.sale_detail, name='sale_detail'),
        path('sale/<int:sale_id>/receipt/', views.generate_receipt, name='generate_receipt'),
        path('sales/branch/<str:branch_name>/', views.sales_by_branch, name='sales_by_branch'),
        path('manager/matugga/', views.manager_dashboard_matugga, name='manager_dashboard_matugga'),
        path('manager/maganjo/', views.manager_dashboard_maganjo, name='manager_dashboard_maganjo'),
        path('salesagent/matugga/', views.sales_agent_dashboard_matugga, name='sales_agent_dashboard_matugga'),
        path('salesagent/maganjo/', views.sales_agent_dashboard_maganjo, name='sales_agent_dashboard_maganjo'),
        path('login/', views.Login, name='login'),
        path('branch_sales_report/', branch_sales_report, name='branch_sales_report'),
        path('signup/', views.signup, name='signup'),


]

        

