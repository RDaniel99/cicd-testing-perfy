from json_loader.exceptions.invalid_argument import InvalidArgument
from json_loader.rules.json_rule import JSONRule, RuleTypes


class OneOfRule(JSONRule):
    def __init__(self, values_type):
        super().__init__(RuleTypes.ONE_OF, values_type)
        self.valid_values = []

    def validate_rule(self, value):
        if not self.valid_values:
            raise InvalidArgument("Valid values are not set")

        if value is None or not isinstance(value, self.values_type):
            raise InvalidArgument("Value to check is not set")

        return value in self.valid_values
