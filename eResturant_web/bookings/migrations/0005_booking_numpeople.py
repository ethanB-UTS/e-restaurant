# Generated by Django 3.1.7 on 2021-04-08 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0004_auto_20210408_0437'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='numPeople',
            field=models.IntegerField(default=0),
        ),
    ]