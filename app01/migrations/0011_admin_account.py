# Generated by Django 4.1 on 2024-01-12 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app01", "0010_alter_order_admin"),
    ]

    operations = [
        migrations.AddField(
            model_name="admin",
            name="account",
            field=models.CharField(default=1, max_length=64, verbose_name="管理员账号"),
            preserve_default=False,
        ),
    ]
