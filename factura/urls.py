from django.urls import path
from .views import ClienteView, ClienteNew, ClienteEdit, inactivar_cliente, FacturaView, \
    facturas, ProductoView, borrar_detalle_factura

from .reportes import imprimir_factura_recibo, imprimir_factura_list

urlpatterns = [
    path('clientes', ClienteView.as_view(), name='cliente_list'),
    path('clientes/new', ClienteNew.as_view(), name='cliente_new' ),
    path('cliente/edit/<int:pk>/', ClienteEdit.as_view(), name='cliente_edit'),
    path('cliente/delete/<int:cliente_id>/', inactivar_cliente, name='cliente_delete'),

    #path facturas
    path('facturas/', FacturaView.as_view(), name='factura_list'),
    path('facturas/new', facturas, name='factura_new'),
    path('factura/edit/<int:id>/', facturas, name="factura_edit"),
    path('facturas/buscar-producto', ProductoView.as_view(), name='buscar_producto'),

    path('facturas/borrar-detalle/<int:id>', borrar_detalle_factura, name='factura_borrar_detalle'),
    path('factura/imprimir/<int:numero_factura>/', imprimir_factura_recibo, name='factura_imprimir_one'),
    path('facturas/imprimir-todas/<str:f1>/<str:f2>/', imprimir_factura_list, name='factura_imprimir_all')

]