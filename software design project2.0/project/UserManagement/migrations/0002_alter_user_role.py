# Generated by Django 5.0.3 on 2025-02-15 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(max_length=45),
        ),
    ]
