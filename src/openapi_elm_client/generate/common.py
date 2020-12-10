from functools import wraps


def _valid_elm(f):
    """Attempt to create a valid Elm identifier from a string.

    This replaces illegal characters with legal onces.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        result = f(*args, **kwargs)
        # TODO: More replacements.
        result = result.replace('@', 'atsign_')
        if result == 'type':
            result = 'type_'
        return result
    return wrapper


@_valid_elm
def convert_to_pascal_case(value):
    for separator in {'-', '.', ' '}:
        value = value.replace(separator, '_')
    elements = value.split('_')
    return ''.join(map(_upper_first_letter, elements))


@_valid_elm
def convert_to_camel_case(value):
    pc = convert_to_pascal_case(value)
    return _lower_first_letter(pc)


def _upper_first_letter(value):
    return ''.join([c.upper() for c in value[:1]]) + value[1:]


def _lower_first_letter(value):
    return ''.join([c.lower() for c in value[:1]]) + value[1:]
