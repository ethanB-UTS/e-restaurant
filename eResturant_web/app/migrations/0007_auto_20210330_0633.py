# Generated by Django 2.1.4 on 2021-03-30 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_userprofile_isstaff'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='fName',
            new_name='First Name',
        ),
    ]