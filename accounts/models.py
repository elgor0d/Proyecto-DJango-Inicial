from django.db import models
from django.contrib.auth.models import User

class SesionActiva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    ultimo_acceso = models.DateTimeField(auto_now=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.usuario} — {self.ip}"