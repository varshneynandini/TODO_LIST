# Generated by Django 4.2.13 on 2024-06-22 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='status',
            field=models.CharField(choices=[('C', 'COMPLETED'), ('P', 'PENDING')], max_length=2),
        ),
    ]