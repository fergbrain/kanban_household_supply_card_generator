# Generated by Django 3.2.10 on 2021-12-16 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=30)),
                ('rack', models.CharField(max_length=10)),
                ('shelf', models.CharField(max_length=10)),
            ],
            options={
                'ordering': ('region', 'rack', 'shelf'),
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('contact', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(null=True, upload_to='images/')),
                ('additional_information', models.TextField(blank=True, null=True)),
                ('consumption', models.IntegerField(help_text='Weekly')),
                ('time_to_replenish', models.IntegerField(help_text='Days')),
                ('safety_stock', models.IntegerField(help_text='Count')),
                ('reorder_at', models.IntegerField(null=True)),
                ('reorder_qty', models.IntegerField()),
                ('reorder_units', models.CharField(default='ct', max_length=10)),
                ('alt_source_ok', models.BooleanField(default=False, help_text='OK to use different manufacturer?')),
                ('alt_supplier_ok', models.BooleanField(default=False, help_text='OK to buy from different store?')),
                ('supply_type', models.CharField(choices=[('INTERNAL', 'Internal'), ('EXTERNAL', 'External')], default='EXTERNAL', max_length=8)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='card.location')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='card.supplier')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]