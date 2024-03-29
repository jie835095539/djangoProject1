# Generated by Django 4.1 on 2023-12-26 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app01", "0004_userinfo_depart"),
    ]

    operations = [
        migrations.CreateModel(
            name="MobileAccount",
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
                ("mobile", models.CharField(max_length=11, verbose_name="手机号")),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, default=0, max_digits=10, verbose_name="价格"
                    ),
                ),
                (
                    "level",
                    models.SmallIntegerField(
                        choices=[(1, "一星"), (2, "二星"), (3, "三星"), (4, "四星"), (5, "五星")],
                        null=True,
                        verbose_name="级别",
                    ),
                ),
                (
                    "status",
                    models.SmallIntegerField(
                        choices=[(0, "未占用"), (1, "已占用")], null=True, verbose_name="状态"
                    ),
                ),
            ],
        ),
    ]
