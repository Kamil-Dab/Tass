# Generated by Django 3.2.16 on 2023-01-12 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='city_ascii',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='city',
            name='state_name',
            field=models.CharField(max_length=50),
        ),
    ]
