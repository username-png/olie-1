# Generated by Django 3.0.3 on 2020-05-01 19:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_auto_20200501_1839'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Label',
            new_name='Tag',
        ),
        migrations.RenameField(
            model_name='answer',
            old_name='label',
            new_name='tag',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='label',
            new_name='tag',
        ),
    ]
