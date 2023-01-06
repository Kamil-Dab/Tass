# Generated by Django 3.2.16 on 2023-01-06 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itin_id', models.PositiveBigIntegerField()),
                ('mkt_id', models.PositiveBigIntegerField()),
                ('quarter', models.PositiveIntegerField()),
                ('passengers', models.PositiveIntegerField()),
                ('distance', models.PositiveIntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='flights',
            name='dest_airport_id',
        ),
        migrations.RemoveField(
            model_name='flights',
            name='origin_airport_id',
        ),
        migrations.RenameModel(
            old_name='OrginAirport',
            new_name='Airport',
        ),
        migrations.DeleteModel(
            name='DestAirport',
        ),
        migrations.DeleteModel(
            name='Flights',
        ),
        migrations.AddField(
            model_name='flight',
            name='dest_airport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination_airport', to='flights.airport', to_field='code'),
        ),
        migrations.AddField(
            model_name='flight',
            name='origin_airport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='origin_airport', to='flights.airport', to_field='code'),
        ),
    ]