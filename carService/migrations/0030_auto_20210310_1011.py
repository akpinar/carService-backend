# Generated by Django 3.1.7 on 2021-03-10 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carService', '0029_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='surname',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]