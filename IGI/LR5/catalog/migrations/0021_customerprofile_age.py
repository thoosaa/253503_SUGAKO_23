# Generated by Django 5.0.6 on 2024-05-13 19:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0020_customerprofile_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerprofile',
            name='age',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
            preserve_default=False,
        ),
    ]
