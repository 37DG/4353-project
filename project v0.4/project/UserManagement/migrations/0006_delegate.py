# Generated by Django 5.0.3 on 2025-04-11 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagement', '0005_alter_user_cougarid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delegate',
            fields=[
                ('delegateId', models.AutoField(primary_key=True, serialize=False)),
                ('delegateUserEmail', models.CharField(max_length=255)),
                ('delegateFormName', models.CharField(max_length=255)),
                ('delegateTo', models.CharField(max_length=255)),
            ],
        ),
    ]
