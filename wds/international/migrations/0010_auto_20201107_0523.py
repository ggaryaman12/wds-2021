# Generated by Django 3.1.1 on 2020-11-06 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('international', '0009_auto_20201107_0520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='priceperstock',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tradereq',
            name='priceperstock',
            field=models.FloatField(default=0, null=True),
        ),
    ]