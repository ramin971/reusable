# Generated by Django 4.2.6 on 2024-02-10 09:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0002_patient_tracking_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='tracking_code',
            field=models.CharField(max_length=16, null=True, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_tc_code', message='must be 16 digit', regex='^\\d{16}$')]),
        ),
    ]