from json_loader.exceptions.invalid_argument import InvalidArgument


class FieldTypeValidator:

    @staticmethod
    def validate(field_type):
        if not isinstance(field_type, type):
            raise InvalidArgument(f"Value {field_type} for field type is not correct")
