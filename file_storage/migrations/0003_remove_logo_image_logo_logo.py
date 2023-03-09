# Generated by Django 4.1.7 on 2023-03-09 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_storage', '0002_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logo',
            name='image',
        ),
        migrations.AddField(
            model_name='logo',
            name='logo',
            field=models.ImageField(default=1, upload_to='logos'),
            preserve_default=False,
        ),
    ]