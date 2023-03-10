# Generated by Django 3.2.16 on 2023-01-05 23:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DestAirport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.PositiveIntegerField(unique=True)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='OrginAirport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.PositiveIntegerField(unique=True)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Flights',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itin_id', models.PositiveBigIntegerField()),
                ('mkt_id', models.PositiveBigIntegerField()),
                ('quarter', models.PositiveIntegerField()),
                ('passengers', models.PositiveIntegerField()),
                ('distance', models.PositiveIntegerField()),
                ('dest_airport_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flights.destairport', to_field='code')),
                ('origin_airport_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flights.orginairport', to_field='code')),
            ],
        ),
    ]
