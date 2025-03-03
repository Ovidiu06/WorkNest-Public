# Generated by Django 5.1.4 on 2025-02-25 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CoduriCOR',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod', models.CharField(blank=True, max_length=10, null=True)),
                ('functia', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titlu_job', models.CharField(max_length=255)),
                ('companie', models.CharField(max_length=255)),
                ('link', models.URLField()),
                ('platforma', models.CharField(blank=True, max_length=50, null=True)),
                ('data', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ZileLibere',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(max_length=255)),
                ('data', models.DateField(unique=True)),
            ],
        ),
    ]
