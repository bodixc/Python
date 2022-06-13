# Generated by Django 4.0.3 on 2022-03-10 20:16

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Категорія')),
                ('url', models.SlugField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Категорія',
                'verbose_name_plural': 'Категорії',
            },
        ),
        migrations.CreateModel(
            name='Petition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=100, verbose_name='Автор')),
                ('title', models.CharField(max_length=100, verbose_name='Назва')),
                ('text', models.TextField(verbose_name='Зміст')),
                ('creation_date', models.DateField(default=datetime.date.today, verbose_name='Дата створення')),
                ('url', models.SlugField(max_length=100, unique=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='petition_service.category', verbose_name='Категорія')),
            ],
            options={
                'verbose_name': 'Петиція',
                'verbose_name_plural': 'Петиції',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100, verbose_name='Значення')),
            ],
            options={
                'verbose_name': 'Статус',
                'verbose_name_plural': 'Статуси',
            },
        ),
        migrations.CreateModel(
            name='Signature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=100, verbose_name='Прізвище')),
                ('name', models.CharField(max_length=100, verbose_name="Ім'я")),
                ('email', models.EmailField(max_length=254)),
                ('petition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='petition_service.petition', verbose_name='Петиція')),
            ],
            options={
                'verbose_name': 'Підпис',
                'verbose_name_plural': 'Підписи',
            },
        ),
        migrations.AddField(
            model_name='petition',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='petition_service.status', verbose_name='Статус'),
        ),
    ]
