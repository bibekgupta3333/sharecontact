# Generated by Django 3.1.1 on 2020-09-24 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0005_auto_20200924_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='created',
            field=models.DateField(auto_now_add=True),
        ),
    ]
