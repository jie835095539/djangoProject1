# Generated by Django 4.1 on 2023-12-25 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app01", "0003_userinfo_gender"),
    ]

    operations = [
        migrations.AddField(
            model_name="userinfo",
            name="depart",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="app01.department",
            ),
        ),
    ]
