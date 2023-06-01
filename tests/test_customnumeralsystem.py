import pytest

from custom_numbers import custom_numbers as cn


# =========================================== CUSTOMNUMERALSYSTEM TESTS

class TestCustomNumeralSystem():
    r"""CustomNumeralSystem test class."""
    
    def test_empty_argument(self):
        with pytest.raises(Exception):
            sysN = cn.CustomNumeralSystem("")
    
    
    def test_duplicates_in_argument(self):
        with pytest.raises(Exception):
            sysN = cn.CustomNumeralSystem("abcc")
    
    
    def test_repr(self):
        expected = "012"
        sysN = cn.CustomNumeralSystem("012")
        result = str(sysN)
        assert result == expected
    
    
    def test_sign_support(self):
        # Warning: This might change in the future
        expected = False
        sysN = cn.CustomNumeralSystem("012")
        result = sysN.sign_support
        assert result == expected
    
    
    def test_forbidden_characters(self):
        # Warning: These might change in the future
        expected = r"+-*/\s"
        sysN = cn.CustomNumeralSystem("012")
        result = sysN.forbidden_characters
        assert result == expected
    
    
    def test_base(self):
        expected = 3
        sysN = cn.CustomNumeralSystem("012") # Base 3
        result = sysN.base
        assert result == expected
    
    
    def test_number_validation(self):
        expected = True
        sysN = cn.CustomNumeralSystem("paf")
        result = sysN.valid_number("ff") # Valid
        assert result == expected
    
    
    def test_number_validation_negative(self):
        expected = False
        sysN = cn.CustomNumeralSystem("paf")
        result = sysN.valid_number("xx") # Invalid
        assert result == expected
    
    
    def test_number_validation_negative_empty_string(self):
        sysN = cn.CustomNumeralSystem("paf")
        with pytest.raises(Exception):
            result = sysN.valid_number("") # Invalid
