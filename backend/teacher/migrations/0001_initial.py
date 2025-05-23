# Generated by Django 5.2.1 on 2025-05-10 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Teacher",
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
                (
                    "user_id",
                    models.CharField(
                        default="default_user_id", max_length=255, unique=True
                    ),
                ),
                (
                    "identity_type",
                    models.CharField(default="default_identity_type", max_length=50),
                ),
                (
                    "identity_value",
                    models.CharField(default="default_identity_value", max_length=255),
                ),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_login", models.DateTimeField(auto_now=True)),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("male", "Male"),
                            ("female", "Female"),
                            ("other", "Other"),
                        ],
                        max_length=10,
                        null=True,
                    ),
                ),
                ("age", models.PositiveIntegerField(blank=True, null=True)),
                ("subject", models.CharField(blank=True, max_length=100, null=True)),
                ("experience_years", models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
