# Generated by Django 2.1.5 on 2019-03-17 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20190317_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='element',
            name='atributeValues',
            field=models.TextField(),
        ),
    ]
