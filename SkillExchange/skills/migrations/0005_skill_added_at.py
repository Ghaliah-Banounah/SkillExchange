# Generated by Django 5.1.3 on 2024-12-18 15:34

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0004_alter_skill_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='added_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]