# Generated by Django 3.1.5 on 2021-05-26 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_auto_20210526_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='last_invoice',
            field=models.PositiveBigIntegerField(blank=True, default=0, max_length=100),
        ),
    ]
