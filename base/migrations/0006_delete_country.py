# Generated by Django 5.0.6 on 2025-03-15 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0005_country"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Country",
        ),
    ]
