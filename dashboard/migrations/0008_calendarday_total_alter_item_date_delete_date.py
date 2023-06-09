# Generated by Django 4.1.2 on 2022-12-13 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_calendaryear_calendarmonth_calendarday'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendarday',
            name='total',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='date',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.calendarday'),
        ),
        migrations.DeleteModel(
            name='Date',
        ),
    ]
