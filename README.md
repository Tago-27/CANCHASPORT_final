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

## Firebase (notificaciones push)

1. Crear proyecto en https://console.firebase.google.com
2. Ir a Configuracion del proyecto > Cuentas de servicio > Generar clave privada
3. Guardar el JSON como `firebase-credentials.json` en la raiz del proyecto
4. Agregar en `settings.py`:
   ```python
   FIREBASE_CREDENTIALS = BASE_DIR / 'firebase-credentials.json'
   ```
5. Editar `static/js/firebase-messaging.js` y `static/js/firebase-sw.js`
   con los datos de tu proyecto Firebase (apiKey, projectId, etc.)
6. En Firebase > Configuracion > Cloud Messaging > Web Push certificates
   copiar la clave VAPID publica y pegarla en `firebase-messaging.js`

## PDF de reservas

Desde el Panel Admin, boton "Descargar PDF" con opciones:
- Todas las reservas
- Solo pendientes
- Solo confirmadas  
- Solo canceladas

Requiere: `pip install reportlab`
