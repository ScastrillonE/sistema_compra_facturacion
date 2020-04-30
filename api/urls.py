from django.urls import path
from .views import ProductoList, ProductoDetalle

urlpatterns=[
    path('v1/producto/', ProductoList.as_view() , name='producto_detalle'),
    path('v1/producto/<str:codigo>/', ProductoDetalle.as_view(), name='producto_detalle'),

]