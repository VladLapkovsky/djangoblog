"""Telegram bot models configuration."""

from django.db import models

from users.models import CustomUser


class TelegramBotChat(models.Model):
    """Telegram bot chat model."""

    telegram_chat_id = models.CharField(max_length=20, verbose_name='telegram chat id', unique=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)

    def __str__(self) -> str:
        """Return telegram chat id.

        Returns:
            telegram chat id
        """
        return self.telegram_chat_id

    class Meta:
        """Add additional parameters to the TelegramBotChat model."""

        verbose_name_plural = 'telegram bot chats'
        verbose_name = 'telegram bot chat'
        ordering = ['user']
