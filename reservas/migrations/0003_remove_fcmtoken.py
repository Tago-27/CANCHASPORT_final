from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0002_alter_cancha_tipo'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FCMToken',
        ),
    ]
