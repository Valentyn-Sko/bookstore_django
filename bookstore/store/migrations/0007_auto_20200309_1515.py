# Generated by Django 3.0.3 on 2020-03-09 15:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import store.models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20200307_1919'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='latitude',
            field=models.TextField(default='50.45466'),
        ),
        migrations.AddField(
            model_name='review',
            name='longitude',
            field=models.TextField(default='30.5238'),
        ),
        migrations.AlterField(
            model_name='book',
            name='cover_image',
            field=models.ImageField(default='books/empty_cover.jpg', upload_to=store.models.cover_upload_path),
        ),
        migrations.AlterField(
            model_name='book',
            name='publish_date',
            field=models.DateField(default=datetime.datetime(2020, 3, 9, 15, 15, 42, 993417, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='review',
            name='publish_date',
            field=models.DateField(default=datetime.datetime(2020, 3, 9, 15, 15, 42, 995199, tzinfo=utc)),
        ),
    ]
