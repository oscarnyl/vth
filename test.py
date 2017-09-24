from typing import Optional, List, Dict, Tuple

from vth import AutoValidator


class ClassWithInt(AutoValidator):
    integer_value: int


class ClassWithOptional(AutoValidator):
    optional_str: Optional[str]


class ClassWithMultipleFields(AutoValidator):
    str_value: str
    bool_value: bool


class ClassWithList(AutoValidator):
    list_value: List[str]


class ClassWithDict(AutoValidator):
    dict_value: Dict[str, str]


class ClassWithTuple(AutoValidator):
    tuple_value: Tuple[str, int]


class ClassWithComplexType(AutoValidator):
    complex_dict: Dict[str, List[int]]


class ClassWithBytes(AutoValidator):
    byte_value: bytes


class ClassWithValidationFunction(AutoValidator):
    email: str
    _validation_functions = [
        (lambda c: c.email, lambda e: "@" in e)
    ]


class ExampleUser(AutoValidator):
    _id: int
    username: str
    email: str
    friends: List[str]

    def __str__(self):
        return (
            f"id: {self._id}\n"
            f"username: {self.username}\n"
            f"email: {self.email}\n"
            f"friends: {', '.join(self.friends)}\n"
        )


if __name__ == "__main__":
    a = ClassWithInt(1)
    b = ClassWithOptional("foo")
    c = ClassWithOptional(None)
    d = ClassWithMultipleFields("foo", True)
    e = ClassWithList(["foo", "bar"])
    f = ClassWithDict({"foo": "bar", "baz": "bat"})
    g = ClassWithTuple(("asd", 123))
    h = ClassWithComplexType({"foo": [1, 2, 3], "bar": [4, 5, 6]})
    j = ClassWithBytes(b'test')
    k = ClassWithValidationFunction("oscnyl@github.com")
    # k = ClassWithValidationFunction("not_an_email")
    user = ExampleUser(
        1,
        "oscar",
        "oscnyl@github",
        ["someguy", "someotherguy"]
    )
    print(user)
