# Generated by Django 3.1.7 on 2021-06-12 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('headers_temp', '0004_auto_20210606_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='header',
            name='bank',
            field=models.CharField(choices=[('sbl', 'standard bank limited'), ('bcbl', 'bangladesh commercial bank limited'), ('exim', 'Export Import Bank of Bangladesh Limited'), ('jbl', 'Jamuna Bank Ltd')], max_length=8),
        ),
    ]
