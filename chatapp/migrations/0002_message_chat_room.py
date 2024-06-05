# Generated by Django 5.0 on 2024-02-05 09:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chatapp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="chat_room",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="chatapp.chatroom",
            ),
            preserve_default=False,
        ),
    ]
