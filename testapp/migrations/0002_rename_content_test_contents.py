# Generated by Django 4.1.7 on 2023-05-05 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='test',
            old_name='content',
            new_name='contents',
        ),
    ]