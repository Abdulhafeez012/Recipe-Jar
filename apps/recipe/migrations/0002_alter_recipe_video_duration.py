# Generated by Django 4.2.8 on 2024-05-09 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='video_duration',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
