# Generated by Django 3.1.7 on 2021-03-16 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myclubuser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='User Email'),
        ),
    ]