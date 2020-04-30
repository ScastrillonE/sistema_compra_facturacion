from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum

from bases.models import ClaseModelo
from inventario.models import Producto


# Create your models here.
class Proveedor(ClaseModelo):
    descripcion = models.CharField(
        max_length=100,
        unique=True
    )
    direccion = models.CharField(
        max_length=250,
        null=True, blank=True
    )
    contacto = models.CharField(
        max_length=250,
    )
    telefono = models.CharField(
        max_length=10,
        null=True, blank=True
    )
    email = models.CharField(
        max_length=250,
    )

    def save(self):
        self.descripcion = self.descripcion.capitalize()
        super(Proveedor, self).save()

    def __str__(self):
        return '{}'.format(self.descripcion)


class ComprasEnc(ClaseModelo):
    fecha_compra = models.DateField(null=True, blank=True)
    observacion = models.TextField(null=True, blank=True)
    no_factura = models.CharField(max_length=300)
    fecha_factura = models.DateField()
    sub_total = models.FloatField(default=0)
    descuento = models.FloatField(default=0)
    total = models.FloatField(default=0)

    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.observacion)

    def save(self):
        self.observacion = self.observacion.capitalize()
        self.total = self.sub_total - self.descuento
        super(ComprasEnc, self).save()

    class Meta:
        verbose_name = 'Encabezado compra'
        verbose_name_plural = 'Encabezado de compras'


class ComprasDet(ClaseModelo):
    compra = models.ForeignKey(ComprasEnc, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.BigIntegerField(default=0)
    precio_prv = models.FloatField(default=0)
    sub_total = models.FloatField(default=0)
    descuento = models.FloatField(default=0)
    total = models.FloatField(default=0)
    costo = models.FloatField(default=0)

    def __str__(self):
        return '{}'.format(self.producto)

    def save(self):
        self.sub_total = float(float(int(self.cantidad)) * float(self.precio_prv))
        self.total = self.sub_total - float(self.descuento)
        super(ComprasDet, self).save()

    class Meta:
        verbose_name = "Detalle compra"
        verbose_name_plural = "Detalles compras"


@receiver(post_delete, sender=ComprasDet)
def detalle_compra_borrar(sender, instance, **kwargs):
    id_producto = instance.producto.id
    id_compra = instance.compra.id

    enc = ComprasEnc.objects.filter(pk=id_compra).first()
    if enc:
        sub_total = ComprasDet.objects.filter(compra=id_compra).aggregate(Sum('sub_total'))
        descuento = ComprasDet.objects.filter(compra=id_compra).aggregate(Sum('descuento'))
        enc.sub_total = sub_total['sub_total__sum']
        enc.descuento = descuento['descuento__sum']
        enc.save()

    produc = Producto.objects.filter(pk=id_producto).first()
    if produc:
        cantidad = int(produc.existencia) - int(instance.cantidad)
        produc.existencia = cantidad
        produc.save()

@receiver(post_save, sender =ComprasDet)
def detalle_compras_guardar(sender,instance,**kwargs):
    id_producto = instance.producto.id
    fecha_compra = instance.compra.fecha_compra

    produc = Producto.objects.filter(pk=id_producto).first()
    if produc:
        cantidad = int(produc.existencia) + int(instance.cantidad)
        produc.existencia = cantidad
        produc.ultima_compra = fecha_compra
        produc.save()