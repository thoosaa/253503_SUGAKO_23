# Generated by Django 5.0.6 on 2024-05-09 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('CUSTOMER', 'customer'), ('STAFF', 'staff'), ('ADMIN', 'admin')], default='ADMIN', max_length=8),
        ),
    ]
