from json_loader.generators.random_values_generator import *
from json_loader.rules.json_rule import RuleTypes
from json_loader.validators.rules_validator import validate_value_against_rules


def generate_according_to_rule(rule, field_type, percentages):
    if rule.rule_type == RuleTypes.BETWEEN_MIN_MAX:
        return generate_value_in_interval(rule.minimum, rule.maximum, field_type)
    elif rule.rule_type == RuleTypes.LESS_THAN:
        return generate_value_less_than(rule.value_to_be_less_than, field_type)
    elif rule.rule_type == RuleTypes.MORE_THAN:
        return generate_value_more_than(rule.value_to_be_more_than, field_type)
    elif rule.rule_type == RuleTypes.LESS_THAN_OR_EQUAL:
        return generate_value_less_than_or_equal_to(rule.value_to_be_less_than_or_equal, field_type)
    elif rule.rule_type == RuleTypes.MORE_THAN_OR_EQUAL:
        return generate_value_more_than_or_equal_to(rule.value_to_be_more_than_or_equal, field_type)
    elif rule.rule_type == RuleTypes.ONE_OF:
        return generate_from_list_using_percentages(rule.valid_values, percentages)
    elif rule.rule_type == RuleTypes.EQUAL_TO:
        return generate_value_equal_to(rule.value_to_be_equal_to, field_type)
    else:
        raise InvalidArgument(f"Unknown rule {rule.rule_type}")


def are_constraints_met(current_json, current_field, schema):
    if current_field.field_name not in schema.fields_dependencies:
        return False

    dependencies = schema.fields_dependencies[current_field.field_name]
    if len(dependencies) == 0:
        return False

    # TODO: Make it to have more constraints
    dependency = dependencies[0]
    return validate_value_against_rules(current_field.constraints[0]["check"], current_json[dependency])


def generate(schema):
    final_json = {}

    for field_name in schema.get_fields_in_order_of_completion():
        field = schema.json_fields[field_name]

        rules_to_apply = field.rules
        if are_constraints_met(final_json, field, schema):
            rules_to_apply = field.constraints[0]["rules"]

        for rule in rules_to_apply:
            final_json[field.field_name] = generate_according_to_rule(rule, field.field_type, field.percentages)

    return final_json
