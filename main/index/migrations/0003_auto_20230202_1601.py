# Generated by Django 3.1.8 on 2023-02-02 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_attendance_mark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='DateNow',
            field=models.DateField(auto_now=True),
        ),
    ]
