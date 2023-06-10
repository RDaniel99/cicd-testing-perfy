import random
import string

from json_loader.exceptions.invalid_argument import InvalidArgument


def generate_from_list_using_percentages(values, percentages):

    if percentages is None or len(percentages) == 0:
        return generate_from_list(values)

    return random.choices(values, percentages)[0]


def generate_from_list(values):
    return random.choice(values)


def generate_value_in_interval(minimum, maximum, value_type):
    if value_type == int:
        return random.randint(minimum, maximum)

    if value_type == float:
        return random.uniform(minimum, maximum)

    raise InvalidArgument(f"Can not generate random value in an interval for value type {value_type}")


def generate_value_less_than(value, value_type):
    if value_type == int:
        return random.randint(int(-1e18), value - 1)

    if value_type == float:
        return random.uniform(float(-1e18), value)

    raise InvalidArgument(f"Can not generate random value less than {value} for value type {value_type}")


def generate_value_less_than_or_equal_to(value, value_type):
    if value_type == int:
        return random.randint(int(-1e18), value)
    elif value_type == float:
        return random.uniform(float(-1e18), value)
    else:
        raise InvalidArgument(
            f"Cannot generate random value less than or equal to {value} for value type {value_type}")


def generate_value_more_than(value, value_type):
    if value_type == int:
        return random.randint(value + 1, int(1e18))
    elif value_type == float:
        return random.uniform(value, float(1e18))
    else:
        raise InvalidArgument(f"Cannot generate random value more than {value} for value type {value_type}")


def generate_value_more_than_or_equal_to(value, value_type):
    if value_type == int:
        return random.randint(value, int(1e18))
    elif value_type == float:
        return random.uniform(value, float(1e18))
    else:
        raise InvalidArgument(
            f"Cannot generate random value more than or equal to {value} for value type {value_type}")


def generate_value_equal_to(value, value_type):
    if value is None:
        raise InvalidArgument("Value can not be None")

    if not isinstance(value, value_type):
        raise InvalidArgument(f"Value {value} is not of type {value_type}")

    return value


def generate_random_string_with_digits_and_letters(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def generate_random_string_with_letters_only(length):
    characters = string.ascii_letters
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string
