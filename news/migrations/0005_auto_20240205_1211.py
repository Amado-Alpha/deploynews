# Generated by Django 3.2.21 on 2024-02-05 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_20240203_1341'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Mytests',
        ),
        migrations.DeleteModel(
            name='Newupdates',
        ),
    ]