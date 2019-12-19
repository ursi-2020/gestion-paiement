# Generated by Django 3.0 on 2019-12-19 17:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0008_auto_20191111_1102'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduledCredits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.TextField()),
                ('amount', models.IntegerField(default=0)),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
        migrations.RemoveField(
            model_name='incident',
            name='message',
        ),
        migrations.AlterField(
            model_name='incident',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]