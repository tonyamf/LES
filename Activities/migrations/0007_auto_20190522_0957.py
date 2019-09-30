# Generated by Django 2.1.7 on 2019-05-22 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Activities', '0006_auto_20190415_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='sentence',
            name='artefactid',
            field=models.ForeignKey(blank=True, db_column='ArtefactID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Activities.Artefact', verbose_name='Artefacto'),
        ),
        migrations.AddField(
            model_name='sentence',
            name='resourceid',
            field=models.ForeignKey(blank=True, db_column='ResourceID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Activities.Resource', verbose_name='Recurso'),
        ),
    ]
