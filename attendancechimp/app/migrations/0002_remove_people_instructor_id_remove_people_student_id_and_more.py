# Generated by Django 5.1 on 2024-11-15 21:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='people',
            name='instructor_id',
        ),
        migrations.RemoveField(
            model_name='people',
            name='student_id',
        ),
        migrations.AlterField(
            model_name='qr_codes',
            name='lecture',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.lecture'),
        ),
    ]