# Generated by Django 3.0.2 on 2020-01-24 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=36)),
                ('second_name', models.CharField(max_length=36)),
                ('birthday', models.DateField()),
                ('password', models.CharField(max_length=16)),
            ],
        ),
    ]