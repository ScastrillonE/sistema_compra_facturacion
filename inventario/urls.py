from django.urls import path

from .views import (
    CategoriaView,
    CategoriaNew,
    CategoriaEdit,
    categoria_inactivar,
    #CategoriaDelete,
    SubCategoriaView,
    SubCategoriaNew,
    SubCategoriaEdit,
    subcategoria_inactivar,
    #SubCategoriaDelete,
    MarcaView,
    MarcaNew,
    MarcaEdit,
    marca_inactivar,
    UnidadMedidaView,
    UnidadMedidaNew,
    UnidadMedidaEdit,
    unidad_inactivar,
    ProductoView,
    producto_inactivar,
    ProductoNew,
    ProductoEdit,
)

urlpatterns = [
    path('categorias/', CategoriaView.as_view(), name='categoria_list'),
    path('categorias/new/', CategoriaNew.as_view(), name='categoria_new'),
    path('categorias/edit/<int:pk>/', CategoriaEdit.as_view(), name='categoria_edit'),
    path('categoria/delete/<int:id>/', categoria_inactivar, name='categoria_delete'),
    # Path Subcategorias
    path('subcategoria/', SubCategoriaView.as_view(), name='subcategoria_list'),
    path('subcategoria/new/', SubCategoriaNew.as_view(), name='subcategoria_new'),
    path('subcategoria/edit/<int:pk>/', SubCategoriaEdit.as_view(), name='subcategoria_edit'),
    path('subcategoria/delete/<int:pk>/', subcategoria_inactivar , name='subcategoria_delete'),
    # Path Marca
    path('marcas/', MarcaView.as_view(), name='marca_list'),
    path('marcas/new/', MarcaNew.as_view(), name='marca_new'),
    path('marca/edit/<int:pk>/', MarcaEdit.as_view(), name='marca_edit'),
    path('marca/delete/<int:id>', marca_inactivar, name='marca_delete'),
    # Path Unidad de medida
    path('unidades/medida', UnidadMedidaView.as_view(), name='unidad_medida_list'),
    path('unidad/medida/new/', UnidadMedidaNew.as_view(), name='unidad_medida_new'),
    path('unidad/medida/edit/<int:pk>/', UnidadMedidaEdit.as_view(), name='unidad_medida_edit'),
    path('unidad/medida/delete/<int:id>/', unidad_inactivar, name='unidad_medida_delete'),
    # Path Producto
    path('productos/', ProductoView.as_view(), name='producto_list'),
    path('producto/new/', ProductoNew.as_view(), name='producto_new'),
    path('producto/edit/<int:pk>/', ProductoEdit.as_view(), name='producto_edit'),
    path('producto/delete/<int:id>/', producto_inactivar, name='producto_delete'),

]
