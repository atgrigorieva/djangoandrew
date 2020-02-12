# Generated by Django 2.1.5 on 2019-03-17 12:36

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0003_auto_20190217_1736'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribut',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('hasValue', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('atributeValues', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('favicon', models.FileField(upload_to='favicons/')),
                ('keywords', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('elements', models.ManyToManyField(to='base.Element')),
            ],
        ),
        migrations.CreateModel(
            name='TypeElement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('tag', models.CharField(max_length=50)),
                ('isPairTag', models.BooleanField(default=True)),
                ('attributs', models.ManyToManyField(to='base.Attribut')),
            ],
        ),
        migrations.RemoveField(
            model_name='puresite',
            name='favicon',
        ),
        migrations.RemoveField(
            model_name='puresite',
            name='title',
        ),
        migrations.AddField(
            model_name='puresite',
            name='master',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='page',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.PureSite'),
        ),
        migrations.AddField(
            model_name='element',
            name='elementType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.TypeElement'),
        ),
    ]