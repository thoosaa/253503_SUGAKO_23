# Generated by Django 5.0.6 on 2024-05-13 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0019_feedback_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerprofile',
            name='name',
            field=models.CharField(default=1, max_length=300),
            preserve_default=False,
        ),
    ]
