# Generated by Django 3.1.5 on 2021-05-18 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_auto_20210515_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellstock',
            name='sell_inventory',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
