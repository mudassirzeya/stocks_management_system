# Generated by Django 3.1.5 on 2021-05-26 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_auto_20210526_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.company'),
        ),
    ]
