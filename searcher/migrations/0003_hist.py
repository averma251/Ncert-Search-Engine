# Generated by Django 4.1 on 2022-11-18 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("searcher", "0002_qa_delete_data"),
    ]

    operations = [
        migrations.CreateModel(
            name="hist",
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
                ("cur_time", models.DateTimeField(auto_now_add=True)),
                ("cur_user", models.TextField()),
                ("cur_question", models.TextField()),
            ],
        ),
    ]
