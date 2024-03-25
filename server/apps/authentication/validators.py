import string
from rest_framework.validators import ValidationError

def include_digit(password):
    is_valid = True
    tests_passed = [number in password for number in string.digits]
    if any(tests_passed):
        return is_valid
    else:
        raise ValidationError("a password must include at least one digit")


def include_upper_letter(password):
    is_valid = True
    tests_passed = [upper_letter in password for upper_letter in string.ascii_uppercase]
    if any(tests_passed):
        return is_valid
    else:
        raise ValidationError("a password must include at least one uppercase letter")
