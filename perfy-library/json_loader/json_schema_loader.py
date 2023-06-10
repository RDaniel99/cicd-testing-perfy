import json

from json_loader.generators.json_schema_generator import generate
from json_loader.json_field import JSONField
from json_loader.json_schema import JSONSchema
from json_loader.rules.between_min_max_rule import BetweenMinMaxRule
from json_loader.rules.equal_to_rule import EqualToRule
from json_loader.rules.less_than_or_equal_to_rule import LessThanOrEqualToRule
from json_loader.rules.less_than_rule import LessThanRule
from json_loader.rules.more_than_or_equal_to_rule import MoreThanOrEqualToRule
from json_loader.rules.more_than_rule import MoreThanRule
from json_loader.rules.one_of_rule import OneOfRule

type_mapping = {
    "string": str,
    "float": float,
    "integer": int,
    "boolean": bool
}


def rule_loader(type_rule, properties, field_type):
    parsed_rule = None
    if type_rule == "betweenMinMax":
        parsed_rule = BetweenMinMaxRule(field_type)
        parsed_rule.maximum = field_type(properties["maximum"])
        parsed_rule.minimum = field_type(properties["minimum"])
    if type_rule == "oneOf":
        parsed_rule = OneOfRule(field_type)
        parsed_rule.valid_values = [field_type(x) for x in properties]
    if type_rule == "lessThan":
        parsed_rule = LessThanRule(field_type)
        parsed_rule.value_to_be_less_than = field_type(properties)
    if type_rule == "lessThanOrEqualTo":
        parsed_rule = LessThanOrEqualToRule(field_type)
        parsed_rule.value_to_be_less_than_or_equal = field_type(properties)
    if type_rule == "moreThan":
        parsed_rule = MoreThanRule(field_type)
        parsed_rule.value_to_be_more_than = field_type(properties)
    if type_rule == "moreThanOrEqualTo":
        parsed_rule = MoreThanOrEqualToRule(field_type)
        parsed_rule.value_to_be_more_than_or_equal = field_type(properties)
    if type_rule == "equalTo":
        parsed_rule = EqualToRule(field_type)
        parsed_rule.value_to_be_equal_to = field_type(properties)

    return parsed_rule


class JSONSchemaLoader:
    def __init__(self, filename="schema.json"):
        self.filename = filename

    def load_json_schema(self):
        try:
            with open(self.filename, "r") as file:
                schema_data = json.load(file)
            return schema_data
        except FileNotFoundError:
            raise Exception(f"File '{self.filename}' not found")
        except json.JSONDecodeError:
            raise Exception(f"Invalid JSON format in '{self.filename}'")

    def parse_json_schema(self):
        json_schema = self.load_json_schema()
        schema = JSONSchema()
        for field_name, field_properties in json_schema.items():
            field = JSONField(field_name)
            field.set_type(type_mapping[field_properties["type"]])

            # Load rules
            if "rules" in field_properties:
                for rule_type, rule_properties in field_properties["rules"].items():
                    field.add_rule(rule_loader(rule_type, rule_properties, field.field_type))

            # Load percentages
            if "percentages" in field_properties:
                for entry in field_properties["percentages"]:
                    field.add_percentage(entry)

            # Load constraints
            if "constraints" in field_properties:
                for entry in field_properties["constraints"]:
                    dependent_to = entry["field"]
                    check_rules = []
                    for rule_type, rule_properties in entry["check"].items():
                        check_rules.append(
                            rule_loader(rule_type, rule_properties, schema.json_fields[dependent_to].field_type))

                    dependent_to_rules = []
                    for rule_type, rule_properties in entry["rules"].items():
                        dependent_to_rules.append(rule_loader(rule_type, rule_properties, field.field_type))

                    field.add_constraint({
                        "field": dependent_to,
                        "check": check_rules,
                        "rules": dependent_to_rules
                    })

                    schema.add_dependency(field_name, dependent_to)

            schema.add_field(field)

        return schema


# loader = JSONSchemaLoader("schema.json")
# parsed_schema = loader.parse_json_schema()

# print(generate(parsed_schema))
