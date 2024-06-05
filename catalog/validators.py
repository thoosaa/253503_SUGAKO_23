import re
from django.core.exceptions import ValidationError


def validate_phone_number_format(value):
    pattern = r'^\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}$'
    if not re.match(pattern, value):
        raise ValidationError('Неверный формат номера телефона. Пожалуйста, введите номер в формате +375 (29) XXX-XX-XX.')