# Generated by Django 5.0.3 on 2025-04-11 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagement', '0004_user_cougarid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='cougarID',
            field=models.IntegerField(null=True),
        ),
    ]
