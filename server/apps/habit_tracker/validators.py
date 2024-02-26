from rest_framework.validators import ValidationError


def validate__not_none(variable):
    is_valid = variable != None
    if not is_valid:
        raise ValidationError(f"The key is not found")
    return is_valid


def validate__length(variable, max_len: int):
    is_valid = 0 < len(variable) <= max_len
    if not is_valid:
        raise ValidationError(
            f'Variable "{variable}" ({len(variable)}) length out of range (1:{max_len})'
        )
    return is_valid


def validate__type(variable, var_type):
    is_valid = type(variable) == var_type
    if not is_valid:
        raise ValidationError(
            f"Type error, expected {var_type}, instead found {type(variable)}"
        )
    return is_valid


def validate_habit_name(variable):
    validators = [
        validate__not_none,
        lambda x: validate__type(x, str),
        lambda x: validate__length(x, 50),
    ]

    tests_passed = [func(variable) for func in validators]
    return all(tests_passed)


def validate_habit_record_value(variable):
    validators = [
        validate__not_none,
        lambda x: validate__type(x, str),
        lambda x: validate__length(x, 30),
    ]

    tests_passed = [func(variable) for func in validators]
    return all(tests_passed)
