# Generated by Django 2.0.2 on 2018-02-24 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
                ('strategy', models.CharField(choices=[('multi_arbitrage', 'Multi Arbitrage'), ('fixed_income', 'Fixed Income'), ('long_short_equity', 'Long Short Equity'), ('event_driven', 'Event Driven')], max_length=100)),
                ('region_exposure', models.CharField(choices=[('global', 'Global'), ('us', 'US'), ('asia', 'Asia')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='FundReturn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.DateField()),
                ('percentage', models.FloatField()),
                ('fund', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='returns_series', to='edgefolio.Fund')),
            ],
        ),
    ]
