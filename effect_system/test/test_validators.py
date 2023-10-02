from . import *
from ..content.validators import *


def test_validator_validates():
    class TrueValidator(Validator):
        def _eval(self, event_data):
            return True

    true_validator = TrueValidator()
    res = true_validator.validate({})
    assert res == True


def test_validator_inverted():
    class TrueValidator(Validator):
        def _eval(self, event_data):
            return True

    false_validator = TrueValidator().invert()
    res = false_validator.validate({})
    assert res == False


def test_validator_property_equals():
    val_one_validator = PropertyEquals("val", 1)
    not_x_ten_validator = PropertyEquals("x", 10).invert()

    event_data1 = {"val": 1, "x": 10}
    res1 = val_one_validator.validate(event_data1)
    res2 = not_x_ten_validator.validate(event_data1)
    assert res1 == True
    assert res2 == False

    event_data2 = {"val": 3, "x": 12}
    res1 = val_one_validator.validate(event_data2)
    res2 = not_x_ten_validator.validate(event_data2)
    assert res1 == False
    assert res2 == True

    y_ten_validator = PropertyEquals("y", 10)
    res3 = y_ten_validator.validate(event_data2)
    assert res3 == False


def test_validator_or():
    val_one_validator = PropertyEquals("val", 1)
    x_ten_validator = PropertyEquals("x", 10)

    or_validator = OrValidator(val_one_validator, x_ten_validator)
    assert len(or_validator._validators) == 2
    assert val_one_validator in or_validator._validators
    assert x_ten_validator in or_validator._validators

    assert or_validator.validate({}) == False
    assert or_validator.validate({"val": 0, "x": 4}) == False
    assert or_validator.validate({"val": 1, "x": 4}) == True
    assert or_validator.validate({"val": 0, "x": 10}) == True
    assert or_validator.validate({"val": 1, "x": 10}) == True


def test_validator_property_one_of():
    arr = []
    x_in_arr_validator = PropertyOneOf("x", arr)

    assert x_in_arr_validator.validate({"y": 10}) == False
    assert x_in_arr_validator.validate({"x": 10}) == False
    arr.append(10)
    assert x_in_arr_validator.validate({"x": 10}) == True


def test_property_in_range():
    x_one_to_ten_validator = PropertyInRange("x", min=1, max=10)
    assert x_one_to_ten_validator.validate({}) == False
    assert x_one_to_ten_validator.validate({"y": 5}) == False
    assert x_one_to_ten_validator.validate({"x": 0}) == False
    assert x_one_to_ten_validator.validate({"x": 1}) == True
    assert x_one_to_ten_validator.validate({"x": 5}) == True
    assert x_one_to_ten_validator.validate({"x": 10}) == True
    assert x_one_to_ten_validator.validate({"x": 20}) == False
