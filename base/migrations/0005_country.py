# Generated by Django 5.0.6 on 2025-03-14 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0004_guestentry_is_read"),
    ]

    operations = [
        migrations.CreateModel(
            name="Country",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("capital", models.CharField(max_length=255)),
                ("population", models.IntegerField()),
                ("currency", models.CharField(max_length=60)),
                ("flag_url", models.URLField()),
            ],
        ),
    ]
