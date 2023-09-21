from test import *


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


def test_validator_event_property_equals():
    val_one_validator = PropertyEquals("val", 1)
    not_x_ten_validator = PropertyEquals("x", 10).invert()

    event_data1 = {"val": 1, "x": 10}
    res1 = val_one_validator.validate(event_data1)
    res2 = not_x_ten_validator.validate(event_data1)
    assert res1 == True
    assert res2 == False

    event_data1 = {"val": 3, "x": 12}
    res1 = val_one_validator.validate(event_data1)
    res2 = not_x_ten_validator.validate(event_data1)
    assert res1 == False
    assert res2 == True
