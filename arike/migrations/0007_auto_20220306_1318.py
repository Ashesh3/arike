# Generated by Django 3.2.12 on 2022-03-06 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arike', '0006_alter_patient_expired_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='familydetail',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default='male', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='familydetail',
            name='relation',
            field=models.CharField(choices=[('brother', 'Brother'), ('sister', 'Sister'), ('husband', 'Husband'), ('wife', 'Wife'), ('mother', 'Mother'), ('son', 'Son'), ('daughter', 'Daughter'), ('uncle', 'Uncle'), ('aunt', 'Aunt'), ('nephew', 'Nephew'), ('niece', 'Niece'), ('cousin', 'Cousin'), ('other', 'Other')], max_length=100),
        ),
    ]