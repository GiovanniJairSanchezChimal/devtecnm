from django.urls import path
from . import views



urlpatterns = [
    
    path('ingresos/registrar/', views.registrar_ingreso, name='registrar_ingreso'),
    
    path('gastos/registrar/', views.registrar_gasto, name='registrar_gasto'),
    
    path('categorias_gasto/registrar/', views.registrar_categoria_gasto, name='registrar_categoria_gasto'),
    
    path('ahorros/registrar/', views.registrar_ahorro, name='registrar_ahorro'),
    
    path('inversiones/registrar/', views.registrar_inversion, name='registrar_inversion'),
   
    path('presupuestos/registrar/', views.registrar_presupuesto, name='registrar_presupuesto'),
    
    path('deudas/registrar/', views.registrar_deuda, name='registrar_deuda'),
    
    path('transacciones/registrar/', views.registrar_transaccion, name='registrar_transaccion'),

    path('reporte_mensual_finanzas/', views.reporte_mensual_finanzas, name='reporte_mensual_finanzas'),
]
