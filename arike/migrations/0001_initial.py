# Generated by Django 3.2.12 on 2022-03-04 08:20

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('full_name', models.CharField(max_length=100)),
                ('role', models.CharField(choices=[('district_admin', 'District Admin'), ('primary_nurse', 'Primary Nurse'), ('secondary_nurse', 'Secondary Nurse')], max_length=100)),
                ('phone', models.IntegerField()),
                ('is_verified', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('icds_code', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LocalBody',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('kind', models.CharField(max_length=100)),
                ('lsg_body_code', models.IntegerField(choices=[(1, 'Grama Panchayath'), (2, 'Block Panchayath'), (3, 'District Panchayath'), (4, 'Nagar Panchayath'), (10, 'Municipality'), (20, 'Corporation'), (50, 'Others')])),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arike.district')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('full_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('address', models.CharField(max_length=255)),
                ('landmark', models.CharField(max_length=100)),
                ('phone', models.IntegerField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=100)),
                ('emergency_phone_number', models.IntegerField()),
                ('expired_time', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('dosage', models.CharField(max_length=100)),
                ('note', models.CharField(max_length=100)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arike.patient')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('number', models.IntegerField()),
                ('local_body', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='arike.localbody')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VisitSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arike.patient')),
                ('visitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VisitDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('palliative_phase', models.CharField(max_length=100)),
                ('blood_pressure', models.CharField(max_length=100)),
                ('pulse', models.CharField(max_length=100)),
                ('general_random_blood_sugar', models.CharField(max_length=100)),
                ('personal_hygiene', models.CharField(max_length=100)),
                ('mouth_hygiene', models.CharField(max_length=100)),
                ('pubic_hygiene', models.CharField(max_length=100)),
                ('systemic_examination', models.CharField(max_length=100)),
                ('patient_at_peace', models.BooleanField(default=False)),
                ('pain', models.BooleanField(default=False)),
                ('symptoms', models.CharField(max_length=100)),
                ('note', models.CharField(max_length=100)),
                ('visit_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arike.visitschedule')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TreatmentNotes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('note', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('treatment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arike.treatment')),
                ('visit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arike.visitdetails')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='treatment',
            name='visit_details',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arike.visitdetails'),
        ),
        migrations.CreateModel(
            name='PatientDisease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('note', models.CharField(max_length=100)),
                ('disease', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arike.disease')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arike.patient')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='patient',
            name='ward',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arike.ward'),
        ),
        migrations.CreateModel(
            name='FamilyDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('full_name', models.CharField(max_length=100)),
                ('phone', models.IntegerField()),
                ('date_of_birth', models.DateField()),
                ('email', models.EmailField(max_length=100)),
                ('relation', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255)),
                ('education', models.CharField(max_length=100)),
                ('occupation', models.CharField(max_length=100)),
                ('remarks', models.CharField(max_length=100)),
                ('is_primary', models.BooleanField(default=False)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arike.patient')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('kind', models.CharField(choices=[('phc', 'Primary Health Centers'), ('chc', 'Community Health Centers')], max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255)),
                ('pincode', models.IntegerField()),
                ('phone', models.IntegerField()),
                ('ward', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arike.ward')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='district',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arike.state'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='arike.district'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='facility',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='arike.facility'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]