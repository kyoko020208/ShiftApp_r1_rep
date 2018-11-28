# Generated by Django 2.1.3 on 2018-11-27 10:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20181127_1022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authuser',
            name='email',
        ),
        migrations.AddField(
            model_name='authuser',
            name='phone',
            field=models.CharField(default=django.utils.timezone.now, max_length=30, unique=True, verbose_name='phone'),
            preserve_default=False,
        ),
    ]