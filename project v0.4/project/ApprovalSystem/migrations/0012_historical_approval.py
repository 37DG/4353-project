# Generated by Django 5.0.3 on 2025-04-12 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ApprovalSystem', '0011_graduate_petition_undergraduate_transfer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Historical_approval',
            fields=[
                ('approval_id', models.AutoField(primary_key=True, serialize=False)),
                ('path', models.CharField(max_length=255)),
            ],
        ),
    ]
