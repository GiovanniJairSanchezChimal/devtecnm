from django.urls import path
from . import views
from .views import detalle_pedido, registrar_abono, reporte_semanal,reporte_mensual

urlpatterns=[
   path('pedido/<int:pedido_id>/', detalle_pedido, name='detalle_pedido'),
   path('pedido/<int:pedido_id>/registrar_abono/', registrar_abono, name='registrar_abono'),
   path('pedido/<int:pedido_id>/editar/', views.editar_pedido, name='editar_pedido'),
   path('pedido/<int:pedido_id>/eliminar/', views.eliminar_pedido, name='eliminar_pedido'),
   path('reporte_semanal/', reporte_semanal, name='reporte_semanal'),
   path('reporte_mensual/', reporte_mensual, name='reporte_mensual'),
   path('pedidos_semanales/', views.lista_pedidos_semanal, name='lista_pedidos_semanal'),
   path('productos/', views.lista_productos, name='lista_productos'),
   path('productos/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
   path('productos/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
   path('clientes/', views.lista_clientes, name='lista_clientes'),
   path('clientes/editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
   path('clientes/eliminar/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
]