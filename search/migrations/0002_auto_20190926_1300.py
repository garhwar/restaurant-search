# Generated by Django 2.2.5 on 2019-09-26 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
