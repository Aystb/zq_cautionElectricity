# Generated by Django 4.2.10 on 2024-02-14 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('password', models.IntegerField(max_length=32)),
                ('electricity', models.IntegerField(max_length=32)),
                ('completedItems', models.IntegerField(max_length=32)),
                ('shutDownCount', models.IntegerField(max_length=32)),
            ],
        ),
    ]
