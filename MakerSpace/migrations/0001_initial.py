# Generated by Django 4.1.4 on 2023-04-09 16:41

import MakerSpace.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
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
                ("title", models.CharField(blank=True, max_length=100, null=True)),
                ("author", models.CharField(max_length=100)),
                ("like", models.IntegerField(default=0)),
                ("description", models.TextField(blank=True, null=True)),
                ("book_category", models.CharField(max_length=50, null=True)),
                ("published_date", models.DateField(auto_now=True)),
                ("public_status", models.BooleanField(default=False)),
                ("sid", models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(db_index=True, max_length=200)),
            ],
            options={
                "verbose_name": "category",
                "verbose_name_plural": "categories",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Stylebase",
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
                ("name", models.CharField(max_length=50)),
                ("styleID", models.CharField(max_length=20)),
                ("stylePrompt", models.CharField(max_length=255)),
                (
                    "style_preview",
                    models.ImageField(upload_to=MakerSpace.models.get_img_name),
                ),
                ("scale", models.IntegerField(default=7)),
                ("steps", models.IntegerField(default=50)),
            ],
        ),
        migrations.CreateModel(
            name="Userinfo",
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
                ("name", models.CharField(blank=True, max_length=50, null=True)),
                ("UserID", models.CharField(blank=True, max_length=50, null=True)),
                ("head_shot", models.ImageField(blank=True, null=True, upload_to="")),
            ],
        ),
        migrations.CreateModel(
            name="PromptBase",
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
                ("keyword", models.CharField(db_index=True, max_length=200)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="promptbase",
                        to="MakerSpace.category",
                    ),
                ),
            ],
            options={"ordering": ("category", "keyword"),},
        ),
        migrations.CreateModel(
            name="Image",
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
                ("page_number", models.PositiveSmallIntegerField()),
                ("image", models.TextField(blank=True, null=True)),
                ("prompt", models.CharField(max_length=255)),
                ("height", models.IntegerField(default=512)),
                ("width", models.IntegerField(default=512)),
                ("steps", models.IntegerField(default=50)),
                ("seeds", models.IntegerField(default=512, null=True)),
                ("scale", models.IntegerField(default=7)),
                ("description", models.TextField(blank=True, null=True)),
                ("img_location", models.TextField(null=True)),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="MakerSpace.book",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="book",
            name="userinfo",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="MakerSpace.userinfo"
            ),
        ),
    ]
