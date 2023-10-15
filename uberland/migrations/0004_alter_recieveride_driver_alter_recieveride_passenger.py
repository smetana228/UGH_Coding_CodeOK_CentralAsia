# Generated by Django 4.1.6 on 2023-10-09 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('uberland', '0003_alter_recieveride_driver_alter_recieveride_passenger'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recieveride',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uberland.driver'),
        ),
        migrations.AlterField(
            model_name='recieveride',
            name='passenger',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uberland.passenger'),
        ),
    ]
