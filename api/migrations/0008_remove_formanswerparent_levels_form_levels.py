# Generated by Django 5.0.4 on 2024-05-12 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_formanswerparent_levels'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formanswerparent',
            name='levels',
        ),
        migrations.AddField(
            model_name='form',
            name='levels',
            field=models.ManyToManyField(blank=True, null=True, to='api.level'),
        ),
    ]
