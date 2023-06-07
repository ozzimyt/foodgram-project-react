from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models
from django.db.models import F, CharField, EmailField, Q

from foodgram.consts import EMAIL_MAX_LENGTH, USER_MAX_LENGTH
from .validators import validate_username


class User(AbstractUser):
    """Кастомная модель пользователя."""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name',)

    username = CharField(
        verbose_name='Имя пользователя',
        help_text='Введите имя пользователя',
        max_length=USER_MAX_LENGTH,
        validators=[validate_username],
        unique=True
    )
    first_name = CharField(
        verbose_name='Имя',
        help_text='Введите имя',
        max_length=USER_MAX_LENGTH,
        blank=True
    )
    last_name = CharField(
        verbose_name='Фамилия',
        help_text='Введите фамилию',
        max_length=USER_MAX_LENGTH,
        blank=True
    )
    email = EmailField(
        verbose_name='Адрес электронной почты',
        help_text='Введите адрес электронной почты',
        unique=True,
        max_length=EMAIL_MAX_LENGTH,
        validators=[EmailValidator]
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username} {self.email}'


class Follow(models.Model):
    """Модель подписчиков."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='follower',
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='following',
    )

    class Meta:
        ordering = ('user', 'author',)
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_follow'
            ),
            models.CheckConstraint(
                check=~Q(user=F('author')),
                name='no_self_subscription'
            )
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
