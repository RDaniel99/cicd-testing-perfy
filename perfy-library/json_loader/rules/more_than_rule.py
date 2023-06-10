from json_loader.exceptions.invalid_argument import InvalidArgument
from json_loader.rules.json_rule import JSONRule, RuleTypes


class MoreThanRule(JSONRule):
    def __init__(self, values_type):
        super().__init__(RuleTypes.MORE_THAN, values_type)
        self.value_to_be_more_than = None

    def validate_rule(self, value):
        if self.value_to_be_more_than is None or not isinstance(self.value_to_be_more_than, self.values_type):
            raise InvalidArgument("Value to be more than is not set")

        if value is None or not isinstance(value, self.values_type):
            raise InvalidArgument("Value to check is not set")

        return value > self.value_to_be_more_than
