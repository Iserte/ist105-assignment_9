from django.contrib import admin
from django.urls import path, include
from dna_center_cisco import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.show_token, name='home'),  # root URL now points to show_token
    path('token/', views.show_token, name='show_token'),
    path('devices/', views.list_devices, name='list_devices'),
    path('interfaces/', views.show_interfaces, name='show_interfaces'),
]