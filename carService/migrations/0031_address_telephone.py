# Generated by Django 3.1.7 on 2021-03-10 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carService', '0030_auto_20210310_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='telephone',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]