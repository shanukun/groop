# Generated by Django 4.1.6 on 2023-02-16 00:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0003_alter_profile_id_alter_relationship_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="avatar",
            field=models.ImageField(default="avatars/avatar.png", upload_to="avatars/"),
        ),
    ]
