from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ClaseModelo(models.Model):
    estado = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_modification = models.IntegerField(blank=True, null=True)

    class Meta:
        abstract = True