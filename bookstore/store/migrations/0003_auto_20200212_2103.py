import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20200210_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='publish_date',
            field=models.DateField(default=datetime.datetime(2020, 2, 12, 21, 3, 31, 474720, tzinfo=utc)),
        ),
    ]