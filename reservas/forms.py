from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Cancha, Reserva
import datetime


class RegistroForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'})
    )
    first_name = forms.CharField(
        max_length=50, required=True, label='Nombre',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'})
    )
    last_name = forms.CharField(
        max_length=50, required=True, label='Apellido',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu apellido'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre de usuario'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contrasena'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmar contrasena'})
        self.fields['username'].label = 'Usuario'
        self.fields['password1'].label = 'Contrasena'
        self.fields['password2'].label = 'Confirmar contrasena'


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre de usuario'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contrasena'})
        self.fields['username'].label = 'Usuario'
        self.fields['password'].label = 'Contrasena'


class CanchaForm(forms.ModelForm):
    class Meta:
        model = Cancha
        fields = ['nombre', 'tipo', 'descripcion', 'precio_hora', 'hora_apertura', 'hora_cierre', 'disponible']
        labels = {
            'nombre': 'Nombre de la cancha',
            'tipo': 'Tipo de deporte',
            'descripcion': 'Descripcion',
            'precio_hora': 'Precio por hora ($)',
            'hora_apertura': 'Hora de apertura',
            'hora_cierre': 'Hora de cierre',
            'disponible': 'Disponible para reservas',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Cancha Norte 1'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio_hora': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '50000'}),
            'hora_apertura': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_cierre': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['fecha', 'hora_inicio', 'hora_fin']
        labels = {
            'fecha': 'Fecha de reserva',
            'hora_inicio': 'Hora de inicio',
            'hora_fin': 'Hora de fin',
        }
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }

    def __init__(self, *args, cancha=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.cancha = cancha
        hoy = datetime.date.today().isoformat()
        self.fields['fecha'].widget.attrs['min'] = hoy

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')

        if fecha and fecha < datetime.date.today():
            raise forms.ValidationError('La fecha no puede ser en el pasado.')

        if hora_inicio and hora_fin:
            if hora_fin <= hora_inicio:
                raise forms.ValidationError('La hora de fin debe ser despues de la hora de inicio.')

            if self.cancha:
                if hora_inicio < self.cancha.hora_apertura:
                    raise forms.ValidationError(f'La cancha abre a las {self.cancha.hora_apertura.strftime("%H:%M")}.')
                if hora_fin > self.cancha.hora_cierre:
                    raise forms.ValidationError(f'La cancha cierra a las {self.cancha.hora_cierre.strftime("%H:%M")}.')

                solapadas = Reserva.objects.filter(
                    cancha=self.cancha,
                    fecha=fecha,
                    estado__in=['pendiente', 'confirmada']
                )
                for r in solapadas:
                    if hora_inicio < r.hora_fin and hora_fin > r.hora_inicio:
                        raise forms.ValidationError(
                            f'Ya existe una reserva de {r.hora_inicio.strftime("%H:%M")} a {r.hora_fin.strftime("%H:%M")} en ese horario.'
                        )

        return cleaned_data
