from django.urls import path
from .views import ProveedorNew, ProveedorView, ProveedorEdit, proveedor_inactivar,\
    ComprasView, compras, CompraDetDelete

from .reportes import reporte_compras, reporte_compra
urlpatterns = [
    path('proveedores/', ProveedorView.as_view(), name='proveedor_list'),
    path('proveedor/new/', ProveedorNew.as_view(), name='proveedor_new'),
    path('proveedor/edit/<int:pk>/', ProveedorEdit.as_view(), name='proveedor_edit'),
    path('proveedor/delete/<int:id>/', proveedor_inactivar, name='proveedor_delete'),
    #Path compras
    path('compras/', ComprasView.as_view(), name='compras_list'),
    path('compras/new', compras, name='compras_new'),
    path('compras/edit/<int:compra_id>', compras, name='compras_edit'),
    path('compras/<int:compra_id>/delete/<int:pk>/', CompraDetDelete.as_view(), name='compras_delete'),

    #Path reportes
    path('compras/reporte', reporte_compras, name='compras_report_all' ),
    path('compra/<int:compra_id>/reporte', reporte_compra, name="compras_report_one")


]