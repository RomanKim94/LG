# Generated by Django 5.0.3 on 2024-03-29 21:23

import tfidf.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TextFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=tfidf.models.TextFile.get_file_name, verbose_name='Text file')),
            ],
        ),
    ]
