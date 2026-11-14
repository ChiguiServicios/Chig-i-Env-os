from django.db import models
from django.contrib.auth.models import User

roles = [
    ("gerente", "Gerente"),
    ("operador", "Operador Integral"),
    ("transportista", "Transportista"),
    ("cliente", "Cliente")
]

class Perfil(models.Model):
    cedula = models.CharField(max_length=9, unique=True)
    telefono = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(null=True, max_length=200, blank=True)
    rol = models.CharField(max_length=200, null=False, choices=roles, default='cliente')
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')

class Meta:
    verbose_name = "Perfil"
    verbose_name_plural = "Perfiles"

def __str__(self):
    return f"{self.cedula} - {self.rol}"