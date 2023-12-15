from django.db import models
from django.contrib.auth.models import AbstractUser


class UsuarioPersonalizado(AbstractUser):
    fec_nac = models.DateField(null=True, blank=True)
    salario = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    def __str__(self):
        return self.username


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
