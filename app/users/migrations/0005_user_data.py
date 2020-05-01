# Generated by Django 3.0.3 on 2020-05-01 18:08

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20191210_0212'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='data',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict),
        ),
    ]
