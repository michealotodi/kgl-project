from django.urls import path
from kglapp import views 
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('about/', views.about, name='about'), 
    path('login/',auth_views.LoginView.as_view(template_name='login.html')),

]
