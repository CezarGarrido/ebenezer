# Generated by Django 4.2.20 on 2025-04-10 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0002_report_alter_donation_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Criado em'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Atualizado em'),
        ),
    ]
