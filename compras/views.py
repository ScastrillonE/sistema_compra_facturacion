from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView,DeleteView
from django.contrib.auth.decorators import login_required, permission_required
import datetime

from django.db.models import Sum

from .models import Proveedor, ComprasDet, ComprasEnc
from .forms import ProveedorForm, ComprasEncForm
from inventario.models import Producto

from bases.views import SinPrivilegiosTemplate


# Create your views here.

class ProveedorView(SinPrivilegiosTemplate, ListView):
    permission_required = 'compras.view_proveedor'
    model = Proveedor
    template_name = 'compras/proveedor_list.html'
    context_object_name = 'obj'
    login_url = 'login'


class ProveedorNew(SinPrivilegiosTemplate, CreateView):
    permission_required = 'compras.add_proveedor'
    model = Proveedor
    template_name = 'compras/proveedor_form.html'
    context_object_name = 'obj'
    form_class = ProveedorForm
    success_url = reverse_lazy('proveedor_list')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.user = self.request.user
        print(self.request.user.id)
        return super().form_valid(form)


class ProveedorEdit(SinPrivilegiosTemplate, UpdateView):
    permission_required = 'compras.change_proveedor'
    model = Proveedor
    template_name = 'compras/proveedor_form.html'
    context_object_name = 'obj'
    form_class = ProveedorForm
    success_url = reverse_lazy('proveedor_list')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.user_modification = self.request.user.id
        print(self.request.user.id)
        return super().form_valid(form)


@login_required(login_url='/login/')
@permission_required('compras.change_proveedor', login_url='/login/')
def proveedor_inactivar(request, id):
    proveedor = Proveedor.objects.filter(pk=id).first()
    context = {}
    template_name = "inventario/catalogo_delete.html"

    if not proveedor:
        return redirect('proveedor_list')

    if request.method == 'GET':
        context['catalogo_obj'] = proveedor

    if request.method == 'POST':
        proveedor.estado = False
        proveedor.save()
        return redirect('proveedor_list')

    return render(request, template_name, context)


class ComprasView(SinPrivilegiosTemplate, ListView):
    permission_required = 'compras.view_comprasenc'
    model = ComprasEnc
    template_name = 'compras/compras_list.html'
    context_object_name = 'obj'
    login_url = 'login'



@login_required(login_url='/login/')
@permission_required('compras.change_compraenc', login_url='/sinprivilegios/')
def compras(request, compra_id=None):
    template_name = 'compras/compras.html'
    producto = Producto.objects.filter(estado=True)
    form_compras = {}
    context = {}

    if request.method == 'GET':
        form_compras = ComprasEncForm()
        enc = ComprasEnc.objects.filter(id=compra_id).first()

        if enc:
            detalle = ComprasDet.objects.filter(compra=enc)
            fecha_compra = datetime.date.isoformat(enc.fecha_compra)
            fecha_factura = datetime.date.isoformat(enc.fecha_factura)
            datos_form = {
                'fecha_compra': fecha_compra,
                'proveedor': enc.proveedor,
                'observacion': enc.observacion,
                'no_factura': enc.no_factura,
                'fecha_factura': fecha_factura,
                'sub_total': enc.sub_total,
                'descuento': enc.descuento,
                'total': enc.total
            }
            form_compras = ComprasEncForm(datos_form)
        else:
            detalle = None

        context = {'productos': producto, 'encabezado': enc, 'detalle': detalle, 'form_enc': form_compras}

    if request.method == 'POST':
        fecha_compra = request.POST.get("fecha_compra")
        observacion = request.POST.get("observacion")
        no_factura = request.POST.get("no_factura")
        fecha_factura = request.POST.get("fecha_factura")
        proveedor = request.POST.get("proveedor")
        sub_total = 0
        descuento = 0
        total = 0

        if not compra_id:
            prov = Proveedor.objects.get(pk=proveedor)

            enc = ComprasEnc(
                fecha_compra=fecha_compra,
                observacion=observacion,
                no_factura=no_factura,
                fecha_factura=fecha_factura,
                proveedor=prov,
                user=request.user
            )

            if enc:
                enc.save()
                compra_id = enc.id
        else:
            enc = ComprasEnc.objects.filter(pk=compra_id).first()
            if enc:
                enc.fecha_compra =fecha_compra
                enc.observacion = observacion
                enc.no_factura = no_factura
                enc.fecha_factura = fecha_factura
                enc.user_modification = request.user.id
                enc.save()

        if not compra_id:
            return redirect('compras_list')

        producto = request.POST.get("id_id_producto")
        cantidad = request.POST.get("id_cantidad_detalle")
        precio = request.POST.get("id_precio_detalle")
        sub_total = request.POST.get("id_subtotal_detalle")
        descuento_detalle =request.POST.get("id_descuento_detalle")
        total_detalle = request.POST.get("id_total_detalle")

        prod = Producto.objects.get(pk=producto)

        det = ComprasDet(
            compra = enc,
            producto = prod,
            cantidad = cantidad,
            precio_prv = precio,
            descuento = descuento_detalle,
            costo = 0,
            user= request.user
        )

        if det:
            det.save()

            sub_total = ComprasDet.objects.filter(compra=compra_id).aggregate(Sum('sub_total'))
            descuento = ComprasDet.objects.filter(compra=compra_id).aggregate(Sum('descuento'))
            enc.sub_total = sub_total["sub_total__sum"]
            enc.descuento = descuento["descuento__sum"]
            enc.save()

        return redirect("compras_edit", compra_id=compra_id)

    return render(request, template_name, context)

class CompraDetDelete(SinPrivilegiosTemplate, DeleteView):
    permission_required = 'compras.delete_comprasdet'
    model = ComprasDet
    template_name = 'compras/compra_det_delete.html'
    context_object_name =  'obj'

    def get_success_url(self):
        compra_id=self.kwargs['compra_id']
        return reverse_lazy('compras_edit', kwargs={'compra_id':compra_id})
