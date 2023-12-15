from django.contrib import admin
from .models import Task
from .models import UsuarioPersonalizado

# Register your models here.


admin.site.register(UsuarioPersonalizado)
admin.site.register(Task)
