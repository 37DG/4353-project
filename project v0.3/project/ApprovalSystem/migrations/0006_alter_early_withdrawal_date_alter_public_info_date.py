# Generated by Django 5.0.3 on 2025-02-28 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ApprovalSystem', '0005_alter_early_withdrawal_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='early_withdrawal',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='public_info',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
