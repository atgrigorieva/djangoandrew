# Generated by Django 2.1.5 on 2019-03-31 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_auto_20190327_1923'),
    ]

    operations = [
        migrations.AddField(
            model_name='attribut',
            name='isStyle',
            field=models.BooleanField(default=True),
        ),
    ]