# Generated by Django 5.0.4 on 2024-04-08 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0004_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='receiver',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='messages',
            name='sender',
            field=models.IntegerField(),
        ),
    ]
