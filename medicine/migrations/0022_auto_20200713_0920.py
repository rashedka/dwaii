# Generated by Django 3.0.7 on 2020-07-13 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0021_auto_20200713_0908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_info',
            name='phone_number',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='user_info',
            name='whatsappNumber',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
