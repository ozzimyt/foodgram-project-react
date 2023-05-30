import re

from django.core.exceptions import ValidationError

REGEX = r'[\w\.@+-]+'


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            'Введите другое имя пользователя'
        )
    entered_name = set(re.sub(REGEX, r'', value.join(set(value))))
    if entered_name:
        raise ValidationError(
            f'Username содержит недопустимые символы: '
            f'{entered_name}'
            ' Допускается использовать только символы алфавита a-z, A-Z'
            ', цифры 0-9 и спецсиволы @, +, - '
        )
    return value
