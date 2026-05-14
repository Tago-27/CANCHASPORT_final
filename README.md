# CanchasSport — Sistema de Reservas

## Instalacion rapida

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install Django reportlab firebase-admin
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## URLs

| URL | Descripcion |
|-----|-------------|
| `/` | Inicio — listado de canchas |
| `/login/` | Iniciar sesion |
| `/registro/` | Crear cuenta |
| `/mis-reservas/` | Reservas del cliente |
| `/panel/` | Panel administrador |
| `/panel/descargar-pdf/?estado=todas` | Descargar PDF de reservas |



## PDF de reservas

Desde el Panel Admin, boton "Descargar PDF" con opciones:
- Todas las reservas
- Solo pendientes
- Solo confirmadas  
- Solo canceladas

Requiere: `pip install reportlab`
