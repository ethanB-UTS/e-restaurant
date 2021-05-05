# Generated by Django 3.1.7 on 2021-05-05 06:27

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookingStartDateTime', models.DateTimeField(default=datetime.datetime.now)),
                ('bookingEndDateTime', models.DateTimeField(default=datetime.datetime.now)),
                ('guests', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('category', models.CharField(choices=[('E', 'Entree'), ('M', 'Main'), ('D', 'Dessert'), ('+', 'Extra(s)')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maxCapacity', models.IntegerField()),
                ('isBooked', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='userProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('First Name', models.CharField(max_length=50)),
                ('Last Name', models.CharField(max_length=50)),
                ('isStaff', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MealOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='app.menu')),
                ('table', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='app.booking')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='table',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='app.table'),
        ),
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
