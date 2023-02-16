# Generated by Django 3.0.6 on 2020-06-01 15:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0002_relationship"),
        ("posts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="liked",
            field=models.ManyToManyField(
                blank=True, related_name="likes", to="profiles.Profile"
            ),
        ),
    ]
