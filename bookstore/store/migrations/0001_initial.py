# Generated by Django 3.0.3 on 2020-02-10 20:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('publish_date', models.DateField(default=datetime.datetime(2020, 2, 10, 20, 41, 49, 234065, tzinfo=utc))),
            ],
        ),
    ]