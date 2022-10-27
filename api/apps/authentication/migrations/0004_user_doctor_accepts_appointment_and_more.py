# Generated by Django 4.1.2 on 2022-10-27 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0003_user_with_google"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="doctor_accepts_appointment",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="user",
            name="doctor_changes_appointment",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="user",
            name="doctor_deletes_appointment",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="user",
            name="prefer_dark_mode",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="user",
            name="vacation_mode",
            field=models.BooleanField(default=False),
        ),
    ]
