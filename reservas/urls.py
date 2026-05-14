from django.urls import path
from . import views

urlpatterns = [
    # Publicas
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.iniciar_sesion, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),

    # Cliente
    path('reservar/<int:cancha_id>/', views.hacer_reserva, name='hacer_reserva'),
    path('mis-reservas/', views.mis_reservas, name='mis_reservas'),
    path('cancelar-reserva/<int:reserva_id>/', views.cancelar_reserva, name='cancelar_reserva'),

    # Admin
    path('panel/', views.admin_panel, name='admin_panel'),
    path('panel/agregar-cancha/', views.agregar_cancha, name='agregar_cancha'),
    path('panel/editar-cancha/<int:cancha_id>/', views.editar_cancha, name='editar_cancha'),
    path('panel/eliminar-cancha/<int:cancha_id>/', views.eliminar_cancha, name='eliminar_cancha'),
    path('panel/reserva/<int:reserva_id>/estado/', views.cambiar_estado_reserva, name='cambiar_estado_reserva'),
    path('panel/descargar-pdf/', views.descargar_pdf_reservas, name='descargar_pdf_reservas'),
]
