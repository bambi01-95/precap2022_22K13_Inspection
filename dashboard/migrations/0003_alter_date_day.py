# Generated by Django 4.1.2 on 2022-12-06 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_alter_date_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='date',
            name='day',
            field=models.TimeField(),
        ),
    ]
