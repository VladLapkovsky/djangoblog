# Generated by Django 3.2.9 on 2021-12-10 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tg_bot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegrambotchat',
            name='telegram_chat_id',
            field=models.CharField(max_length=20, unique=True, verbose_name='telegram chat id'),
        ),
    ]