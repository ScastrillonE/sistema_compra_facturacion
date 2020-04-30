from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required, permission_required

from .models import Categoria, SubCategoria, Marca, UnidadMedida, Producto
from .forms import CategoriaForm, SubCategoriaForm, MarcaForm, UnidadMedidaForm, ProductoForm

from bases.views import SinPrivilegiosTemplate

# Create your views here.
class CategoriaView(SinPrivilegiosTemplate, ListView):
    permission_required = "inventario.view_categoria"
    model = Categoria
    template_name = 'inventario/categoria_list.html'
    context_object_name = 'category'
    


class CategoriaNew(SinPrivilegiosTemplate, SuccessMessageMixin, CreateView):
    permission_required = 'inventario.add_categoria'
    model = Categoria
    template_name = 'inventario/categoria_form.html'
    context_object_name = 'category'
    form_class = CategoriaForm
    success_url = reverse_lazy('categoria_list')
    success_message = "Categoria creada correctamente"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CategoriaEdit(SinPrivilegiosTemplate, SuccessMessageMixin, UpdateView):
    permission_required = 'inventario.change_categoria'
    model = Categoria
    template_name = 'inventario/categoria_form.html'
    context_object_name = 'category'
    form_class = CategoriaForm
    success_url = reverse_lazy('categoria_list')
    success_message = "Categoria actualizada correctamente"


    def form_valid(self, form):
        form.instance.user_modification = self.request.user.id
        return super().form_valid(form)


# class CategoriaDelete(, DeleteView):
#     model = Categoria
#     template_name = 'inventario/catalogo_delete.html'
#     context_object_name = 'catalogo_obj'
#     success_url = reverse_lazy('categoria_list')
@login_required(login_url='/login/')
@permission_required('inventario.change_categoria', login_url='/login/')
def categoria_inactivar(request, id):
    categoria = Categoria.objects.filter(pk=id).first()
    context = {}
    template_name = "inventario/catalogo_delete.html"

    if not categoria:
        return redirect('categoria_list')

    if request.method == 'GET':
        context['catalogo_obj'] = categoria

    if request.method == 'POST':
        categoria.estado = False
        categoria.save()
        messages.success(request, 'Categoria inactiva')
        return redirect('categoria_list')

    return render(request, template_name, context)


class SubCategoriaView(SinPrivilegiosTemplate, ListView):
    permission_required = "inventario.view_subcategoria"
    model = SubCategoria
    template_name = 'inventario/subcategoria_list.html'
    context_object_name = 'subcategory'
    


class SubCategoriaNew(SinPrivilegiosTemplate, SuccessMessageMixin, CreateView):
    permission_required = 'inventario.add_subcategoria'
    model = SubCategoria
    template_name = 'inventario/subcategoria_form.html'
    context_object_name = 'subcategory'
    form_class = SubCategoriaForm
    success_url = reverse_lazy('subcategoria_list')
    success_message = "Subcategoria creada correctamente"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SubCategoriaEdit(SinPrivilegiosTemplate, SuccessMessageMixin, UpdateView):
    permission_required = 'inventario.change_subcategoria'
    model = SubCategoria
    template_name = 'inventario/subcategoria_form.html'
    context_object_name = 'subcategory'
    form_class = SubCategoriaForm
    success_url = reverse_lazy('subcategoria_list')
    success_message = "Subcategoria actualizada correctamente"

    def form_valid(self, form):
        form.instance.user_modification = self.request.user.id
        return super().form_valid(form)


# class SubCategoriaDelete(, DeleteView):
#     model = SubCategoria
#     template_name = 'inventario/catalogo_delete.html'
#     context_object_name = 'catalogo_obj'
#     success_url = reverse_lazy('categoria_list')
@login_required(login_url='/login/')
@permission_required('inventario.change_subcategoria', login_url='/login/')
def subcategoria_inactivar(request, id):
    subcategoria = SubCategoria.objects.filter(pk=id).first()
    context = {}
    template_name = "inventario/catalogo_delete.html"

    if not subcategoria:
        return redirect('categoria_list')

    if request.method == 'GET':
        context['catalogo_obj'] = subcategoria

    if request.method == 'POST':
        subcategoria.estado = False
        subcategoria.save()
        messages.success(request, 'Subcategoria inactiva')
        return redirect('categoria_list')

    return render(request, template_name, context)

class MarcaView(SinPrivilegiosTemplate, ListView):
    permission_required = "inventario.view_marca"
    model = Marca
    template_name = 'inventario/marca_list.html'
    context_object_name = 'marca'
    


class MarcaNew(SinPrivilegiosTemplate, SuccessMessageMixin, CreateView):
    permission_required = 'inventario.add_marca'
    model = Marca
    template_name = 'inventario/marca_form.html'
    context_object_name = 'marca'
    form_class = MarcaForm
    success_url = reverse_lazy('marca_list')
    success_message = "Marca creada correctamente"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MarcaEdit(SinPrivilegiosTemplate, SuccessMessageMixin, UpdateView):
    permission_required = 'inventario.change_marca'
    model = Marca
    template_name = 'inventario/marca_form.html'
    context_object_name = 'marca'
    form_class = MarcaForm
    success_url = reverse_lazy('marca_list')
    success_message = "Marca actualizada correctamente"


    def form_valid(self, form):
        form.instance.user_modification = self.request.user.id
        return super().form_valid(form)

@login_required(login_url='/login/')
@permission_required('inventario.change_marca', login_url='/login/')
def marca_inactivar(request, id):
    marca = Marca.objects.filter(pk=id).first()
    context = {}
    template_name = "inventario/catalogo_delete.html"

    if not marca:
        return redirect('marca_list')

    if request.method == 'GET':
        context['catalogo_obj'] = marca

    if request.method == 'POST':
        marca.estado = False
        marca.save()
        messages.success(request, 'Marca inactiva')
        return redirect('marca_list')

    return render(request, template_name, context)


class UnidadMedidaView(SinPrivilegiosTemplate, ListView):
    permission_required = "inventario.view_unidadmedida"
    model = UnidadMedida
    template_name = 'inventario/unidad_medida_list.html'
    context_object_name = 'unidad_medida'
    


class UnidadMedidaNew(SinPrivilegiosTemplate, SuccessMessageMixin, CreateView):
    permission_required = 'inventario.add_unidadmedida'
    model = UnidadMedida
    template_name = 'inventario/unidad_medida_form.html'
    context_object_name = 'unidad_medida'
    form_class = UnidadMedidaForm
    success_url = reverse_lazy('unidad_medida_list')
    success_message = "Unidad de medida creada correctamente"


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UnidadMedidaEdit(SinPrivilegiosTemplate, SuccessMessageMixin, UpdateView):
    permission_required = 'inventario.change_unidadmedida'
    model = UnidadMedida
    template_name = 'inventario/unidad_medida_form.html'
    context_object_name = 'unidad_medida'
    form_class = UnidadMedidaForm
    success_url = reverse_lazy('unidad_medida_list')
    success_message = "Unidad de medida actualizada correctamente"


    def form_valid(self, form):
        form.instance.user_modification = self.request.user.id
        return super().form_valid(form)

@login_required(login_url='/login/')
@permission_required('inventario.change_unidadmedida', login_url='/login/')
def unidad_inactivar(request, id):
    unidad = UnidadMedida.objects.filter(pk=id).first()
    context = {}
    template_name = 'inventario/catalogo_delete.html'

    if not unidad:
        return redirect('unidad_medida_list')

    if request.method == 'GET':
        context['catalogo_obj'] = unidad

    if request.method == 'POST':
        unidad.estado = False
        unidad.save()
        messages.success(request, 'Unidad de medida inactiva')
        return redirect('unidad_medida_list')

    return render(request, template_name, context)


class ProductoView(SinPrivilegiosTemplate, ListView):
    permission_required = 'inventario.view_producto'
    model = Producto
    template_name = 'inventario/producto_list.html'
    context_object_name = 'producto'
    


class ProductoNew(SinPrivilegiosTemplate, SuccessMessageMixin, CreateView):
    permission_required = 'inventario.add_producto'
    model = Producto
    template_name = 'inventario/producto_form.html'
    context_object_name = 'producto'
    form_class = ProductoForm
    success_url = reverse_lazy('producto_list')
    success_message = "Producto creado correctamente"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProductoEdit(SinPrivilegiosTemplate, SuccessMessageMixin, UpdateView):
    permission_required = 'inventario.change_producto'
    model = Producto
    template_name = 'inventario/producto_form.html'
    context_object_name = 'producto'
    form_class = ProductoForm
    success_url = reverse_lazy('producto_list')
    success_message = "Producto actualizado correctamente"

    def form_valid(self, form):
        form.instance.user_modification = self.request.user.id
        return super().form_valid(form)

@login_required(login_url='/login/')
@permission_required('inventario.change_producto', login_url='/login/')
def producto_inactivar(request, id):
    producto = Producto.objects.filter(pk=id).first()
    context = {}
    template_name = "inventario/catalogo_delete.html"

    if not producto:
        return redirect('producto_list')

    if request.method == 'GET':
        context['catalogo_obj'] = producto

    if request.method == 'POST':
        producto.estado = False
        producto.save()
        messages.success(request, 'Producto inactivo')
        return redirect('producto_list')

    return render(request, template_name, context)
