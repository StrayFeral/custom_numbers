import pytest

from custom_numbers import custom_numbers as cn


# ================================================== CUSTOMNUMBER TESTS


class TestCustomNumber():
    r"""CustomNumber test class."""
    
    def test_invalid_number(self):
        sysN = cn.CustomNumeralSystem("paf")
        with pytest.raises(Exception):
            num = cn.CustomNumber(sysN, "x") # Invalid
    
    
    def test_repr(self):
        expected = "1100101"
        sysN = cn.CustomNumeralSystem("01")
        num = cn.CustomNumber(sysN, "1100101")
        result = str(num)
        assert result == expected
    
    
    def test_init_value(self):
        expected = "1100101"
        sysN = cn.CustomNumeralSystem("01")
        num = cn.CustomNumber(sysN, "1100101")
        result = str(num.init_value)
        assert result == expected
    
    
    def test_digit_to_int(self):
        expected = 1
        sysN = cn.CustomNumeralSystem("paf") # 0 1 2
        num = cn.CustomNumber(sysN, "aaa")
        result = num.digit_to_int("a")
        assert result == expected
    
    
    def test_digit_to_int_hex(self):
        """Just in case"""
        
        expected = 15
        sysN = cn.CustomNumeralSystem("0123456789abcdef") # Common hex system
        num = cn.CustomNumber(sysN, "aaa")
        result = num.digit_to_int("f")
        assert result == expected
    
    
    def test_digit_to_int_negative_more_characters(self):
        sysN = cn.CustomNumeralSystem("paf") # 0 1 2
        num = cn.CustomNumber(sysN, "aaa")
        with pytest.raises(Exception):
            result = num.digit_to_int("aa")
    
    
    def test_digit_to_int_negative_empty(self):
        sysN = cn.CustomNumeralSystem("paf") # 0 1 2
        num = cn.CustomNumber(sysN, "aaa")
        with pytest.raises(Exception):
            result = num.digit_to_int("")
    
    
    def test_to_decimal_hex(self):
        expected = 240
        sysN = cn.CustomNumeralSystem("0123456789abcdef") # Common hex system
        num = cn.CustomNumber(sysN, "f0")
        result = num.to_decimal()
        assert result == expected
    
    
    def test_to_decimal_bin(self):
        expected = 101
        sysN = cn.CustomNumeralSystem("01") # Common bin system
        num = cn.CustomNumber(sysN, "1100101")
        result = num.to_decimal()
        assert result == expected
    
    
    def test_to_decimal_ternary(self):
        expected = 4
        sysN = cn.CustomNumeralSystem("paf")
        num = cn.CustomNumber(sysN, "aa")
        result = num.to_decimal()
        assert result == expected
