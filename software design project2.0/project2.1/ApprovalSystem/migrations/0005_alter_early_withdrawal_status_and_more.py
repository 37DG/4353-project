# Generated by Django 5.0.3 on 2025-02-28 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ApprovalSystem', '0004_early_withdrawal_name_public_info_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='early_withdrawal',
            name='status',
            field=models.CharField(choices=[('draft', 'draft'), ('pending', 'pending'), ('returned', 'returned'), ('approved', 'approved')], default='draft', max_length=20),
        ),
        migrations.AlterField(
            model_name='public_info',
            name='status',
            field=models.CharField(choices=[('draft', 'raft'), ('pending', 'pending'), ('returned', 'returned'), ('approved', 'approved')], default='draft', max_length=20),
        ),
    ]
