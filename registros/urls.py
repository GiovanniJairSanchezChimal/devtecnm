from django.urls import path
from . import views

urlpatterns =[
    path('registro_productos/', views.registro_productos, name='registro_productos'),
    path('registro_clientes/', views.registro_clientes, name='registro_clientes'),
    path('crear_pedido/', views.crear_pedido, name='crear_pedido'),
    path('registro_categoria/', views.registro_categoria, name='registro_categoria'),
]