from json_loader.exceptions.invalid_argument import InvalidArgument
from json_loader.rules.json_rule import JSONRule, RuleTypes


class EqualToRule(JSONRule):
    def __init__(self, values_type):
        super().__init__(RuleTypes.EQUAL_TO, values_type)
        self.value_to_be_equal_to = None

    def validate_rule(self, value):
        if self.value_to_be_equal_to is None or not isinstance(self.value_to_be_equal_to, self.values_type):
            raise InvalidArgument("Value against to check if equal is not set")

        if value is None or not isinstance(value, self.values_type):
            raise InvalidArgument("Value to check if equal is not set")

        return value == self.value_to_be_equal_to
