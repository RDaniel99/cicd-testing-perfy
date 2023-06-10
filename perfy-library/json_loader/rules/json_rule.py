from enum import Enum

from json_loader.exceptions.invalid_argument import InvalidArgument
from json_loader.validators.field_type_validator import FieldTypeValidator


class JSONRule:
    def __init__(self, rule_type, values_type):
        if not isinstance(rule_type, RuleTypes):
            raise InvalidArgument("Rule type is not correct")
        self.rule_type = rule_type

        FieldTypeValidator.validate(values_type)
        self.values_type = values_type

    def validate_rule(self, value):
        raise NotImplemented("Method JSONRule::validate_rule must be implemented")


class RuleTypes(Enum):
    BETWEEN_MIN_MAX = 1
    EQUAL_TO = 2
    LESS_THAN = 3
    LESS_THAN_OR_EQUAL = 4
    MORE_THAN = 5
    MORE_THAN_OR_EQUAL = 6
    ONE_OF = 7
