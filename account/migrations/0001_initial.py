# Generated by Django 5.0 on 2023-12-09 18:47

import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("idx", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "username",
                    models.CharField(help_text="유저 명", max_length=255, unique=True),
                ),
                ("password", models.CharField(help_text="유저 패스워드", max_length=128)),
                (
                    "is_staff",
                    models.BooleanField(default=False, help_text="staff 권한 여부"),
                ),
                (
                    "is_superuser",
                    models.BooleanField(default=False, help_text="root 권한 여부"),
                ),
                ("is_active", models.BooleanField(default=True, help_text="계정 활성화 여부")),
                (
                    "purchase_car",
                    models.CharField(
                        blank=True, help_text="구매한 차", max_length=100, null=True
                    ),
                ),
                (
                    "sale_car",
                    models.CharField(
                        blank=True, help_text="구매한 차", max_length=100, null=True
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, help_text="생성일", verbose_name="date joined"
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True, help_text="변경일")),
                (
                    "last_login",
                    models.DateTimeField(blank=True, help_text="마지막 로그인", null=True),
                ),
            ],
            options={
                "abstract": False,
            },
            managers=[
                ("object", django.db.models.manager.Manager()),
            ],
        ),
    ]
