# Generated by Django 3.1.7 on 2021-05-11 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_menu_menutype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='menutype',
            field=models.CharField(choices=[('B', 'Breakfast'), ('L', 'Lunch'), ('D', 'Dinner')], max_length=50),
        ),
    ]
