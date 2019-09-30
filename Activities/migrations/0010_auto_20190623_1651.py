# Generated by Django 2.1.7 on 2019-06-23 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Activities', '0009_auto_20190622_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='groupname',
            field=models.CharField(db_column='GroupName', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='sentence',
            name='receiver',
            field=models.CharField(blank=True, db_column='Receiver', max_length=255, verbose_name='Recetor'),
        ),
    ]