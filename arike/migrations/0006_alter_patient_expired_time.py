# Generated by Django 3.2.12 on 2022-03-05 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arike', '0005_alter_patient_expired_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='expired_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
