# Generated by Django 5.1.3 on 2024-12-16 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.SmallIntegerField(choices=[(1, 'Bad'), (2, 'Acceptable'), (3, 'Good'), (4, 'Great'), (5, 'Awesome')]),
        ),
    ]
