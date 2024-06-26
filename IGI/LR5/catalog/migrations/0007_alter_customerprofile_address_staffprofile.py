# Generated by Django 5.0.6 on 2024-05-11 09:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_sale_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerprofile',
            name='address',
            field=models.TextField(max_length=400),
        ),
        migrations.CreateModel(
            name='StaffProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phonenumber', models.CharField(max_length=13)),
                ('email', models.CharField(max_length=70)),
                ('photo', models.ImageField(upload_to='images/')),
                ('proffesion', models.CharField(max_length=200)),
                ('staff', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='catalog.staff')),
            ],
        ),
    ]
