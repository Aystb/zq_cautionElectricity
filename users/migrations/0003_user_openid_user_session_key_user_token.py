# Generated by Django 4.2.10 on 2024-02-20 04:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0002_alter_user_completeditems_alter_user_electricity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='openid',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='session_key',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='token',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
