# Generated by Django 5.1.7 on 2025-05-11 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guides', '0002_guides_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='guidesimages',
            name='video_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
