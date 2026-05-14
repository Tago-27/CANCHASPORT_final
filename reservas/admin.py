from django.contrib import admin
from .models import Cancha, Reserva

@admin.register(Cancha)
class CanchaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'precio_hora', 'hora_apertura', 'hora_cierre', 'disponible']
    list_filter = ['tipo', 'disponible']

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'cancha', 'fecha', 'hora_inicio', 'hora_fin', 'estado']
    list_filter = ['estado', 'fecha']


