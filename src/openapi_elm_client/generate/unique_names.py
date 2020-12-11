"""Support for generating unique names in generated code.
"""

_COUNTER = 0


def unique_name(prefix='val'):
    """Generate a unique name starting with the given prefix.

    Args:
        prefix: A string which the generated name should start with.

    Returns: A unique name starting with `prefix`.

    Raises:
        ValueError: If `prefix` is empty.
    """
    global _COUNTER

    if not prefix:
        raise ValueError('Prefix can not be empty.')

    result = prefix + str(_COUNTER)
    _COUNTER += 1
    return result
