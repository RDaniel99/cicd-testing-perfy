from json_loader.exceptions.invalid_argument import InvalidArgument
from json_loader.rules.json_rule import JSONRule, RuleTypes


class BetweenMinMaxRule(JSONRule):
    def __init__(self, values_type):
        super().__init__(RuleTypes.BETWEEN_MIN_MAX, values_type)
        self.minimum = None
        self.maximum = None

    def validate_rule(self, value):
        if self.minimum is None or not isinstance(self.minimum, self.values_type):
            raise InvalidArgument("Minimum is not set")

        if self.maximum is None or not isinstance(self.maximum, self.values_type):
            raise InvalidArgument("Maximum is not set")

        if value is None or not isinstance(value, self.values_type):
            raise InvalidArgument(f"Value to check is not {self.values_type}")

        return self.minimum <= value <= self.maximum
