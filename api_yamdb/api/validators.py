import re

from rest_framework.exceptions import ValidationError


class MixinValidatorUsername:

    def validate_username(self, value):
        if value.lower() == 'me':
            raise ValidationError('Username не должно быть "me"')
        if value == re.sub(r'^[\w.@+-]+$', r'', value):
            raise ValidationError(
                'Username содержит недопустимые символы {value}'
            )
        return value
