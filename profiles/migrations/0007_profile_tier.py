# Generated by Django 3.1.6 on 2021-03-03 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_auto_20210302_0945'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='tier',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
