# Generated by Django 5.1.1 on 2024-09-20 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raterapi', '0003_remove_picture_image_remove_picture_player_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
