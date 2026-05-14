from django.db import models
from django.contrib.auth.models import User


class Cancha(models.Model):
    TIPOS = [
        ('futbol', 'Fútbol'),
        ('tenis', 'Tenis'),
        ('baloncesto', 'Baloncesto'),
        ('volleyball', 'Volleyball'),
    ]
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPOS, default='futbol')
    descripcion = models.TextField(blank=True)
    precio_hora = models.DecimalField(max_digits=10, decimal_places=2, default=50000)
    hora_apertura = models.TimeField(default='07:00')
    hora_cierre = models.TimeField(default='22:00')
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"

    class Meta:
        verbose_name = 'Cancha'
        verbose_name_plural = 'Canchas'


class Reserva(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas')
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE, related_name='reservas')
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.cancha.nombre} - {self.fecha}"

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['-fecha_creacion']
