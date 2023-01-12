# Generated by Django 3.2.16 on 2023-01-12 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=30)),
                ('city_ascii', models.CharField(max_length=30)),
                ('state_id', models.CharField(max_length=5)),
                ('state_name', models.CharField(max_length=30)),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('population', models.PositiveIntegerField()),
                ('density', models.FloatField()),
                ('timezone', models.CharField(max_length=40)),
            ],
        ),
    ]