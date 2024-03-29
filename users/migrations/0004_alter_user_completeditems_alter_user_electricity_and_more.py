# Generated by Django 4.2.10 on 2024-02-20 09:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0003_user_openid_user_session_key_user_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='completedItems',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='electricity',
            field=models.IntegerField(default=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='shutDownCount',
            field=models.IntegerField(default=0),
        ),
    ]
