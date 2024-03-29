# Generated by Django 4.2 on 2023-04-22 21:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.CharField(blank=True, default=True, max_length=75),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, db_index=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='uid',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]
