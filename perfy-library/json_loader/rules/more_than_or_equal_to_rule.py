from json_loader.exceptions.invalid_argument import InvalidArgument
from json_loader.rules.json_rule import JSONRule, RuleTypes


class MoreThanOrEqualToRule(JSONRule):
    def __init__(self, values_type):
        super().__init__(RuleTypes.MORE_THAN_OR_EQUAL, values_type)
        self.value_to_be_more_than_or_equal = None

    def validate_rule(self, value):
        if self.value_to_be_more_than_or_equal is None or not isinstance(
            self.value_to_be_more_than_or_equal, self.values_type
        ):
            raise InvalidArgument("Value to be more than or equal is not set")

        if value is None or not isinstance(value, self.values_type):
            raise InvalidArgument("Value to check is not set")

        return value >= self.value_to_be_more_than_or_equal
