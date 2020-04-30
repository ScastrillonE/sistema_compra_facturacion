from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView

from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponse
import datetime
from django.contrib import messages
from django.contrib.auth import authenticate

from bases.views import SinPrivilegiosTemplate

from .models import Cliente, FacturaEnc, FacturaDet
from .forms import ClienteForm
from inventario.views import ProductoView
from inventario.models import Producto


# Create your views here.

class ClienteView(SinPrivilegiosTemplate, ListView):
    permission_required = 'factura.view_cliente'
    model = Cliente
    template_name = 'factura/cliente_list.html'
    context_object_name = 'obj'
    login_url = '/login/'


class ClienteNew(SinPrivilegiosTemplate, CreateView):
    permission_required = 'factura.add_cliente'
    model = Cliente
    template_name = 'factura/cliente_form.html'
    context_object_name = 'obj'
    form_class = ClienteForm
    success_url = reverse_lazy('cliente_list')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.user = self.request.user
        print(self.request.user.id)
        return super().form_valid(form)


class ClienteEdit(SinPrivilegiosTemplate, UpdateView):
    permission_required = 'factura.change_cliente'
    model = Cliente
    template_name = 'factura/cliente_form.html'
    context_object_name = 'obj'
    form_class = ClienteForm
    success_url = reverse_lazy('cliente_list')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.user_modification = self.request.user.id
        print(self.request.user.id)
        return super().form_valid(form)


@login_required(login_url='/login/')
@permission_required('factura.change_cliente')
def inactivar_cliente(request, cliente_id):
    cliente = Cliente.objects.filter(pk=cliente_id).first()
    template_name = 'factura/cliente_delete.html'
    context = {}

    if not cliente:
        redirect('cliente_list')

    if request.method == 'GET':
        context['obj_delete'] = cliente

    if request.method == 'POST':
        cliente.estado = False
        cliente.save()
        messages.success(request, 'Cliente inactivado')
        return redirect('cliente_list')

    return render(request, template_name, context)


class FacturaView(SinPrivilegiosTemplate, ListView):
    model = FacturaEnc
    template_name = 'factura/factura_list.html'
    context_object_name = 'obj'
    permission_required = 'factura.view_factura'


@login_required(login_url='/login/')
@permission_required('factura.change_facturasenc', login_url='sinprivilegios')
def facturas(request, id=None):
    template_name = 'factura/facturas.html'
    detalle = {}
    cliente = Cliente.objects.filter(estado=True)

    if request.method == "GET":
        enc = FacturaEnc.objects.filter(pk=id).first()
        if not enc:
            encabezado = {
                'id': 0,
                'fecha': datetime.datetime.today(),
                'cliente': 0,
                'sub_total': 0.00,
                'descuento': 0.00,
                'total': 0.00,
            }
            detalle = None
        else:
            encabezado = {
                'id': enc.id,
                'fecha': datetime.datetime.today(),
                'cliente': enc.cliente,
                'sub_total': enc.sub_total,
                'descuento': enc.descuento,
                'total': enc.total,
            }
            detalle = FacturaDet.objects.filter(factura=enc)

        context = {"enc": encabezado, "det": detalle, "clientes": cliente}

    if request.method == 'POST':
        cliente = request.POST.get("enc_cliente")
        fecha = request.POST.get("fecha")
        clien = Cliente.objects.get(pk=cliente)

        # si no hay id significa que la factura es nueva
        if not id:
            enc = FacturaEnc(
                cliente=clien,
                fecha=fecha,
                user=request.user
            )
            if enc:
                enc.save()
                id = enc.id
        else:
            enc = FacturaEnc.objects.filter(pk=id).first()
            if enc:
                enc.cliente = clien
                enc.user_modification = request.user.id
                enc.save()
        if not id:
            messages.error(request, 'No se detecto ningun numero de factura')
            return redirect('factura_list')

        codigo = request.POST.get('codigo')
        cantidad = request.POST.get('cantidad')
        precio = request.POST.get('precio')
        s_total = request.POST.get('sub_total_detalle')
        descuento = request.POST.get('descuento_detalle')
        total = request.POST.get('total_detalle')

        pro = Producto.objects.get(codigo=codigo)
        det = FacturaDet(
            user=request.user,
            factura=enc,
            producto=pro,
            cantidad=cantidad,
            precio=precio,
            sub_total=s_total,
            descuento=descuento,
            total=total,

        )

        if det:
            det.save()

        return redirect('factura_edit', id=id)

    return render(request, template_name, context)


class ProductoView(ProductoView):
    template_name = "factura/buscar_producto.html"


def borrar_detalle_factura(request, id):
    template_name = 'factura/factura_borrar_detalle.html'
    context = {}

    det = FacturaDet.objects.get(pk=id)

    if request.method == 'GET':
        context = {'det': det}

    if request.method == 'POST':
        usr = request.POST.get('usuario')
        pas = request.POST.get('pass')

        user = authenticate(username=usr, password=pas)

        if not user:
            return HttpResponse("usuario o clave incorrecta")

        if not user.is_active:
            return HttpResponse("usuario Inactivo")

        if user.is_superuser or user.has_perm("sup_caja_facturadet"):
            det.id = None
            det.cantidad = (-1 * det.cantidad)
            det.subtotal = (-1 * det.sub_total)
            det.descuento = (-1 * det.descuento)
            det.total = (-1 * det.total)
            det.save()

            return HttpResponse("ok")
        return HttpResponse("Usuario no autorizado")


    return render(request, template_name, context)
