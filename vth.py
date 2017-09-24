from typing import Any, _Union, List, Dict, Tuple


base_types = [int, str, bool, float, complex, bytes, type(None)]


class Validator:
    def validate(self, silent: bool=False) -> bool:
        for attribute, attr_type in self.__annotations__.items():
            if not self._validate_attribute(attribute, attr_type):
                if not silent:
                    raise ValidationException(
                        f"Invalid attribute: {attribute}, value: "
                        f"{getattr(self, attribute)}"
                    )
                return False
        if hasattr(self, "_validation_functions"):
            for attribute_selector, func in self._validation_functions:
                val = attribute_selector(self)
                if not func(val):
                    if not silent:
                        raise ValidationException(
                            f"Invalid attribute with value {val}"
                        )
                    return False

    def _validate_attribute(self, attribute: str, attr_type: Any) -> bool:
        val = getattr(self, attribute)
        return Validator._validate_value(val, attr_type)

    @staticmethod
    def _validate_value(val, val_type) -> bool:
        if val_type in base_types:
            return isinstance(val, val_type)

        if isinstance(val_type, _Union):
            return Validator._validate_union(val, val_type)
        if issubclass(val_type, List):
            return Validator._validate_list(val, val_type)
        if issubclass(val_type, Dict):
            return Validator._validate_dict(val, val_type)
        if issubclass(val_type, Tuple):
            return Validator._validate_tuple(val, val_type)

    @staticmethod
    def _validate_union(val, union) -> bool:
        for union_member in union.__args__:
            if Validator._validate_value(val, union_member):
                return True
        return False

    @staticmethod
    def _validate_list(lst: List, lst_type_info) -> bool:
        item_type = lst_type_info.__args__[0]
        for item in lst:
            if not Validator._validate_value(item, item_type):
                return False
        return True

    @staticmethod
    def _validate_dict(dct: Dict, dct_type_info) -> bool:
        key_type, value_type = dct_type_info.__args__
        for key, value in dct.items():
            if not Validator._validate_value(key, key_type):
                return False
            if not Validator._validate_value(value, value_type):
                return False
        return True

    @staticmethod
    def _validate_tuple(tpl: Tuple, tpl_type_info) -> bool:
        for val, val_type in zip(tpl, tpl_type_info.__args__):
            if not Validator._validate_value(val, val_type):
                return False
        return True


class AutoValidator(Validator):
    def __init__(self, *args, **kwargs):
        if len(self.__annotations__) != len(args):
            raise ValidationException("Invalid amount of arguments")
        for member, arg in zip(self.__annotations__, args):
            setattr(self, member, arg)
        self.validate()


class ValidationException(Exception):
    pass
