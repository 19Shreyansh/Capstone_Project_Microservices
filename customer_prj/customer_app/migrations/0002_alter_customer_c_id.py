# Generated by Django 5.1.6 on 2025-03-04 05:40

import customer_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='c_id',
            field=models.BigIntegerField(default=customer_app.models.generate_customer_id, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
