from json_loader.validators.field_type_validator import FieldTypeValidator


class JSONField:
    def __init__(self, field_name):
        self.field_name = field_name
        self.field_type = None
        self.percentages = []
        self.rules = []
        self.constraints = []

    def set_type(self, field_type):
        FieldTypeValidator.validate(field_type)

        self.field_type = field_type

    def add_constraint(self, constraint):
        self.constraints.append(constraint)

    def add_percentage(self, percentage):
        self.percentages.append(percentage)

    def add_rule(self, rule):
        self.rules.append(rule)
