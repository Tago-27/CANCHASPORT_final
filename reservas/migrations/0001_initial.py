from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cancha',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('tipo', models.CharField(choices=[('futbol','Futbol'),('tenis','Tenis'),('baloncesto','Baloncesto'),('volleyball','Volleyball')], default='futbol', max_length=20)),
                ('descripcion', models.TextField(blank=True)),
                ('precio_hora', models.DecimalField(decimal_places=2, default=50000, max_digits=10)),
                ('hora_apertura', models.TimeField(default='07:00')),
                ('hora_cierre', models.TimeField(default='22:00')),
                ('disponible', models.BooleanField(default=True)),
            ],
            options={'verbose_name': 'Cancha', 'verbose_name_plural': 'Canchas'},
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('estado', models.CharField(choices=[('pendiente','Pendiente'),('confirmada','Confirmada'),('cancelada','Cancelada')], default='pendiente', max_length=20)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('cancha', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservas', to='reservas.cancha')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservas', to=settings.AUTH_USER_MODEL)),
            ],
            options={'verbose_name': 'Reserva', 'verbose_name_plural': 'Reservas', 'ordering': ['-fecha_creacion']},
        ),
        migrations.CreateModel(
            name='FCMToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.TextField()),
                ('actualizado', models.DateTimeField(auto_now=True)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='fcm_token', to=settings.AUTH_USER_MODEL)),
            ],
            options={'verbose_name': 'Token FCM', 'verbose_name_plural': 'Tokens FCM'},
        ),
    ]
