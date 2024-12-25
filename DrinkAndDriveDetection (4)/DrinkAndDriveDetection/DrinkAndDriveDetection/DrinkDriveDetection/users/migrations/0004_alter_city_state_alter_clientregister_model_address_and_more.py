# Generated by Django 5.0.6 on 2024-12-15 11:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_gender_alter_clientregister_model_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='users.state'),
        ),
        migrations.AlterField(
            model_name='clientregister_model',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='gender',
            name='name',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='state',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='states', to='users.country'),
        ),
    ]