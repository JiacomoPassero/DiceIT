# Generated by Django 4.2.2 on 2023-06-18 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dice',
            name='primary_color',
            field=models.CharField(choices=[('R', 'Red'), ('O', 'Orange'), ('Y', 'Yellow'), ('G', 'Green'), ('B', 'Blue'), ('P', 'Purple'), ('B', 'Black'), ('W', 'White'), ('M', 'Metal')], max_length=1),
        ),
    ]