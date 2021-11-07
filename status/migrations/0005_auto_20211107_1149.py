# Generated by Django 3.2.9 on 2021-11-07 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0004_pullrequest_sha'),
    ]

    operations = [
        migrations.AddField(
            model_name='pullrequest',
            name='test_output',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='pullrequest',
            name='test_status',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='pullrequest',
            name='open',
            field=models.BooleanField(default=True),
        ),
    ]