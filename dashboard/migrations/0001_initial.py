# Generated by Django 4.1.2 on 2022-12-06 11:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('date', models.TimeField()),
            ],
            options={
                'verbose_name_plural': 'answer',
            },
        ),
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField()),
            ],
            options={
                'verbose_name_plural': 'date',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('quantity', models.PositiveBigIntegerField(null=True)),
            ],
            options={
                'verbose_name_plural': 'Product',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15, null=True)),
                ('quan', models.PositiveIntegerField(null=True)),
                ('date', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.date')),
            ],
            options={
                'verbose_name_plural': 'apple',
            },
        ),
    ]
