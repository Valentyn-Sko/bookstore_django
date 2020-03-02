import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc



class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20200217_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='publish_date',
            field=models.DateField(default=datetime.datetime(2020, 2, 20, 20, 53, 53, 830404, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=150, unique=True)),
            ],
            options={
                'ordering': ['last_name'],
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='book',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='book',
            name='publish_date',
            field=models.DateField(default=datetime.datetime(2020, 3, 2, 21, 44, 34, 678374, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(default='')),
                ('publish_date',
                 models.DateField(default=datetime.datetime(2020, 3, 2, 21, 44, 34, 679899, tzinfo=utc))),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('order_date', models.DateField(null=True)),
                ('payment_type', models.CharField(max_length=100, null=True)),
                ('payment_id', models.CharField(max_length=100, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BookOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Book')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Cart')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(blank=True, related_name='books', to='store.Author'),
        ),
        migrations.AddField(
            model_name='book',
            name='genres',
            field=models.ManyToManyField(blank=True, related_name='books', to='store.Genre'),
        ),
    ]