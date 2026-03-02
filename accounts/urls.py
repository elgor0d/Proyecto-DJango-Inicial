from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='home'),  
    path('login/', views.login_view, name='login'),  
    path('logout/', views.logout_view, name='logout'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('user-panel/', views.user_panel, name='user_panel'),
]