# Generated by Django 5.1.4 on 2025-02-25 13:31

import django.db.models.deletion
import recrutare.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('statistici', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(max_length=50)),
                ('prenume', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('numar_telefon', models.CharField(max_length=10)),
                ('CNP', models.CharField(blank=True, max_length=13, null=True)),
                ('judet_candidat', models.CharField(blank=True, max_length=50, null=True)),
                ('localitate_candidat', models.CharField(blank=True, max_length=50, null=True)),
                ('stare_civila', models.CharField(choices=[('necasatorit', 'Necasatorit'), ('casatorit', 'Casatorit'), ('divortat', 'Divortat'), ('vaduv', 'Vaduv'), ('nespecificat', 'Nespecificat')], max_length=20)),
                ('cv', models.FileField(upload_to='cv-uri/', validators=[recrutare.models.validare_fisier_pdf])),
                ('poza', models.ImageField(default='poze_candidati/default.png', upload_to='poze_candidati/')),
                ('data_aplicarii', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('aplicat', 'Aplicat'), ('interviu', 'Interviu'), ('respins', 'Respins'), ('aprobat', 'Aprobat')], default='aplicat', max_length=50)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Companie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Oras',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(max_length=50, verbose_name='Oras')),
            ],
        ),
        migrations.CreateModel(
            name='Departament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(max_length=50, verbose_name='Departament')),
                ('manager', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('manager_group', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.group')),
            ],
        ),
        migrations.CreateModel(
            name='Interviu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_interviu', models.DateField()),
                ('ora_interviu', models.TimeField()),
                ('creat_la', models.DateTimeField(auto_now_add=True)),
                ('candidat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recrutare.candidat')),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creat_la', models.DateTimeField(auto_now_add=True)),
                ('modificat_la', models.DateTimeField(auto_now=True)),
                ('actiunea', models.CharField(choices=[('creat', 'Creat'), ('modificat', 'Modificat'), ('refresh', 'Refresh'), ('reactivare', 'Reactivare'), ('stergere', 'Stergere')], max_length=10)),
                ('url', models.CharField(max_length=150)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pozitie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(max_length=50)),
                ('tip_contract', models.CharField(choices=[('determinat', 'Determinat'), ('nedeterminat', 'Nedeterminat')], default='nedeterminat', max_length=50)),
                ('mod_de_lucru', models.CharField(choices=[('birou', 'Birou'), ('hibrid', 'Hibrid'), ('remote', 'Remote')], default='birou', max_length=50)),
                ('active', models.BooleanField(default=True)),
                ('cod_COR', models.ForeignKey(blank=True, max_length=6, null=True, on_delete=django.db.models.deletion.SET_NULL, to='statistici.coduricor')),
                ('departament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recrutare.departament')),
                ('oras', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='recrutare.oras')),
            ],
        ),
        migrations.AddField(
            model_name='candidat',
            name='pozitie_aplicata',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recrutare.pozitie'),
        ),
        migrations.CreateModel(
            name='StatisticaAdaugareCandidati',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_ora', models.DateTimeField(auto_now_add=True)),
                ('candidat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='recrutare.candidat')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
