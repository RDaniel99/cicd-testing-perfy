from json_loader.exceptions.invalid_argument import InvalidArgument
from json_loader.rules.json_rule import JSONRule, RuleTypes


class LessThanRule(JSONRule):
    def __init__(self, values_type):
        super().__init__(RuleTypes.LESS_THAN, values_type)
        self.value_to_be_less_than = None

    def validate_rule(self, value):
        if self.value_to_be_less_than is None or not isinstance(self.value_to_be_less_than, self.values_type):
            raise InvalidArgument("Value to be less than is not set")

        if value is None or not isinstance(value, self.values_type):
            raise InvalidArgument("Value to check is not set")

        return value < self.value_to_be_less_than
