# Generated by Django 2.1.7 on 2019-06-22 18:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Activities', '0008_auto_20190522_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='userid',
            field=models.ForeignKey(db_column='UserID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]