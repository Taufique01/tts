# Generated by Django 2.2.9 on 2020-01-27 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('texttospeech', '0002_auto_20200127_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='audiofile',
            name='name',
            field=models.CharField(default='unknown', max_length=100),
        ),
        migrations.AlterField(
            model_name='audiofile',
            name='voice_type',
            field=models.CharField(default='wavenet', max_length=100, null=True),
        ),
    ]
