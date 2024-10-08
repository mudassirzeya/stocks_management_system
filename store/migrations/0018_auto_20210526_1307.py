# Generated by Django 3.1.5 on 2021-05-26 07:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0017_company_last_invoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellstock',
            name='invoiceid',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(blank=True, max_length=100)),
                ('customer_id', models.PositiveIntegerField(blank=True, null=True)),
                ('invoice_date', models.CharField(blank=True, max_length=10, null=True)),
                ('due_date', models.CharField(blank=True, max_length=10, null=True)),
                ('discount', models.PositiveBigIntegerField(blank=True, null=True)),
                ('total_bill', models.PositiveBigIntegerField(blank=True, null=True)),
                ('event_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
