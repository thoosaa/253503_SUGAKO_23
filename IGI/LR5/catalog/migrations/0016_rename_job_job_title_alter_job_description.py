# Generated by Django 5.0.6 on 2024-05-12 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0015_job_alter_about_text'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='job',
            new_name='title',
        ),
        migrations.AlterField(
            model_name='job',
            name='description',
            field=models.TextField(max_length=1000),
        ),
    ]
