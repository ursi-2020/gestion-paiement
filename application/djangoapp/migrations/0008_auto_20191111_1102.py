# Generated by Django 2.2.7 on 2019-11-11 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0007_incident_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]
