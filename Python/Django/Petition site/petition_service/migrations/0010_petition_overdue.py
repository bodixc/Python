# Generated by Django 4.0.3 on 2022-04-04 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petition_service', '0009_alter_petition_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='petition',
            name='overdue',
            field=models.BooleanField(default=False, verbose_name='Прострочена'),
        ),
    ]
