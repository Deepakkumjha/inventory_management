from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path,include
from . import views
from .views import CustomLogin

urlpatterns = [
    path('login/',CustomLogin.as_view(template_name='login.html'),name='login'),
    path('admin_page/',views.admin,name='admin'),
    path('worker/',views.worker,name='worker'),
    path('add',views.add,name='add'),
    path('edit/<int:pk>',views.edit,name='edit'),
    path('delete/<int:pk>',views.delete,name='delete'),
    path('assign_product',views.assign_product,name='assign_product'),
    path('see_details/<int:id>',views.see_details,name='see_details'),
    path('register/',views.register,name='register'),
    path('return/<int:id>',views.return_product,name='return'),
    
]