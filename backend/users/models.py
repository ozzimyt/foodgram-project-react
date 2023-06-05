from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models
from django.db.models import CharField, EmailField

# Я вот тут не уверен, как лучше - импрортировать все константы или только
# нужные, лучше выглдит, когда все, тогда сразу понятно, что это константа,
# помимо верхнего регистра, но, по моему скромному опыту - лучше избегать
# полного импорта, указывая только нужные импорты, оставлю на ревью,
# сделаю как скажешь
from backend.foodgram import consts
from .validators import validate_username


class User(AbstractUser):
    """Кастомная модель пользователя."""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name',)

    username = CharField(
        verbose_name='Имя пользователя',
        help_text='Введите имя пользователя',
        max_length=consts.USER_MAX_LENGTH,
        validators=[validate_username],
        unique=True
    )
    first_name = CharField(
        verbose_name='Имя',
        help_text='Введите имя',
        max_length=consts.USER_MAX_LENGTH,
        blank=True
    )
    last_name = CharField(
        verbose_name='Фамилия',
        help_text='Введите фамилию',
        max_length=consts.USER_MAX_LENGTH,
        blank=True
    )
    email = EmailField(
        verbose_name='Адрес электронной почты',
        help_text='Введите адрес электронной почты',
        unique=True,
        max_length=consts.EMAIL_MAX_LENGTH,
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
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_follow'
            )
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
