r"""NAME
    custom_numbers

MODULE REFERENCE
    N/A

DESCRIPTION
    Swiss-army knife for custom numeral systems.
    
    Copyright (c) 2023 Evgueni Antonov. All rights reserved.
    This work is licensed under the terms of the MIT license.
    See LICENSE file.

CLASSES
    CustomNumeralSystem
    CustomNumber
    GearIterator
"""

import re
from typing import List, Generator
import threading
import asyncio
#import multiprocessing as mp
#from ctypes import c_wtypes_p

__version__ = "0.0.1"
__author__ = r"Evgueni Antonov (Evgueni.Antonov@gmail.com)"

# https://www.reddit.com/r/learnmath/comments/13v410v/what_common_known_symbols_a_numeral_system_with/

r"""
from custom_numbers import custom_numbers as cn
sys3 = cn.CustomNumeralSystem("paf")
num1 = cn.CustomNumber(sys3, "a")
num1.to_decimal()
"""


class CustomNumeralSystem:
    r"""Definition of custom numeral systems with basic consistency validation.
    
    Args:
        digits: String of characters to be perceived as digits.
                The character order is important: 'smallest' is the first on the left!
                This string length would be the numeral system base.
                Obviously each "digit" would consist of a single-
                character.
                
                Forbidden characters: -, +, *, / and space
    
    Example:
        sys1 = CustomNumeralSystem("012ab") # Custom Base5 numeral system
        sys2 = CustomNumeralSystem("mab87")
        
        # Details
        sys3 = CustomNumeralSystem("paf") # Custom Base3 numeral system
        # Example counting from the smallest possible value:
        # "p" # "p" assumes to be the analog of the zero
        # "a"
        # "f"
        # "pp"
        # "pa"
        # "pf"
        # "ap"
        # "aa"
        # and so on. You get the idea.
    """
    
    _SIGNSUPPORT: bool = False # Only unsigned integers at the moment
    _FORBIDDENCHARACTERS: str = r"+-*/\s"
    
    
    def __init__(self, digits: str) -> None:
        self._digits: str = digits
        self._base: int = len(digits)
        
        if len(digits) == 0:
            raise ValueError("Empty 'digits' argument given.")
        
        digit_set = set([x for x in digits])
        if len(digits) != len(digit_set):
            raise ValueError("Duplicate characters in the 'digits' argument.")
        
        # I don't need we need to put a limit here. Let the user decide.
        #if self._base > self._MAXBASE:
        #    raise ValueError(f"Unsupported numeral base given {self._base}. Maximum base supported is {self._MAXBASE}.")
        
    
    def __repr__(self) -> str:
        return self._digits
    
    
    @property
    def sign_support(self) -> bool:
        r"""Shows the current state of the sign support - does it support signed numbers?"""
        return self._SIGNSUPPORT
    
    
    @property
    def forbidden_characters(self) -> str:
        return self._FORBIDDENCHARACTERS
    
    
    @property
    def base(self) -> int:
        return self._base
    
    
    def valid_number(self, number: str) -> bool:
        r"""Validation: Is this digit belonging to this numeral system?"""
        
        if len(number) == 0:
            raise ValueError("Passed an empty string as a 'number' argument.")
        
        # Test if string contains forbidden characters
        regex_str = f"\[{self._FORBIDDENCHARACTERS}\]"
        regex = re.compile(regex_str)
        if regex.search(number):
            return False
        
        # Test if string contains any characters outside the defined set
        regex_str = f"\[^{self._digits}\]"
        regex = re.compile(regex_str)
        if regex.search(number):
            return False
        
        return True
    
    

class CustomNumber:
    r"""Definition of a number from the CustomNumericalSystem."""
    
    def __init__(self, numeral_system: CustomNumeralSystem, value: str = "") -> None:
        self._numeral_system: CustomNumeralSystem = numeral_system
        self._init_value: str = value # Just in case we will keep the original value
        self._value: str = self._init_value
        
        if not numeral_system.valid_number(value):
            raise ValueError("Invalid characters in number, which are not in the chosen numeral system.")
    
    
    def __repr__(self) -> str:
        return self._value
    
    
    @property
    def init_value(self) -> str:
        return self._init_value
    
    
    def digit_to_int(self, digit: str) -> int:
        r"""Fastest and simplest possible conversion. Left-most one is the zero."""
        
        if len(digit) != 1:
            raise ValueError("Invalid digit. Contains more than one character.")
        return str(self._numeral_system).index(digit)
    
    
    def to_decimal(self) -> int:
        r"""Converts a number of a custom numeral system to a decimal integer."""
        
        power = 0
        int_value = 0
        
        for digit in self._value[::-1]:
            int_value += self.digit_to_int(digit) * (self._numeral_system.base ** power)
            power += 1
        
        return int_value
    
    
    # input: set of symbols
    # we need to implement:
    # comparison operators < > != == >= etc
    # addition
    # subtraction
    # and maybe refactor the GearIterator class
    # and maybe a method to calculate the number of permutations
    
    # how to prevent more than one asyncio task to read from my iterator?





class GearIterator:
    r"""GearIterator.
    
    Briefly simulates old gear permutators, like the old cars odometer.
    
    The class is serializable, works with both pickle and dill.
    The class implements the context management protocol.
    The class is thread safe.
    
    Args:
        symbol_list: List of symbols. Mind the order of symbols!
        min_length: Minimum length, default is zero
        max_length: Maximum length, default is zero - means no limit
        init_value: Value to initialize with
    
    Returns:
        str
    """
    
    def __init__(self, numeral_system: CustomNumeralSystem, min_length: int = 0, max_length: int = 0, init_value: str = "") -> None:
        self._numeral_system: CustomNumeralSystem = numeral_system
        self._symbol_list: List[str] = [x for x in str(numeral_system)]
        self._min_length = min_length
        self._max_length = max_length
        self._init_value: str = init_value
        self._init_value_returned: bool = False
        self._index: int = 0
        
        # Basic validation ...
        if max_length > 0 and min_length > max_length:
            raise ValueError("min_length is greather than max_length.")
        
        if len(init_value) > 0 and (len(init_value) < min_length or (max_length > 0 and len(init_value) > max_length)):
            raise ValueError("Incorrect init_value length.")
        
        if not numeral_system.valid_number(init_value):
            raise ValueError("Invalid characters in number, which are not in the chosen numeral system.")

        
        self._init_value = init_value[::-1] # Reverse the string
        
        min_len = min_length
        if min_len == 0:
            min_len = 1
        
        self._gears: List[list] = []
        
        # Initialization with init_value
        for symbol in self._init_value:
            seq = self._symbol_list.copy()
            
            while seq[0] != symbol:
                seq.pop(0)
            
            self._gears.append(seq)
        
        # Additional initialization until min_length is reached
        for i in range(len(self._gears), min_len):
            seq = self._symbol_list.copy()
            
            if len(self._init_value) > 0 and i < len(self._init_value):
                symbol = self._init_value[i]
                while seq[0] != symbol:
                    seq.pop(0)
            
            self._gears.append(seq)
        
    
    def __repr__(self) -> str:
        result = ""
        for gear in self._gears:
            result += gear[0]
        return result[::-1] # Reverse the string
    
    
    def __iter__(self) -> object:
        return self
        
    
    # l = list(generator) # internally call next() until exhaustion
    def __next__(self) -> str:
        if not self._init_value_returned:
            self._init_value_returned = True
            return repr(self)
        
        spin_wheels = True
        i = 0
        while spin_wheels:
            self._gears[i].pop(0)
            
            # Reset gear
            if len(self._gears[i]) == 0:
                self._gears[i] = self._symbol_list.copy()
                i += 1
                
                # Add a new gear
                if i == len(self._gears) and i < self._max_length:
                    self._gears.append(self._symbol_list.copy())
                    spin_wheels = False
                
                if i == self._max_length:
                    raise StopIteration
            else: # Wheel not yet reached the final set value
                spin_wheels = False
        
        return repr(self)
    
    
    def __enter__(self) -> object:
        r"""Context management protocol.
        
        Not sure we would need this, but it's there.
        """
        return self
    
    
    def __exit__(self, exc_type, exc_value, exc_tb) -> bool:
        r"""Context management protocol.
        
        StopIteration exception will not be propagated.
        
        Not sure we would need this, but it's there.
        """
        return True # We won't propagate the StopIteration exception




# ~ class GearGenerator:
    # ~ r"""The GearIterator in a generator form."""
    
    # ~ def generate(self, symbol_list: List[str], min_length: int = 0, max_length: int = 0, init_value: str = "") -> Generator[str]:
        # ~ for gear_value in GearIterator(symbol_list, min_length, max_length, init_value):
            # ~ with asyncio.Lock():
                # ~ yield gear_value


# ~ class AsyncGearGenerator:
    # ~ r"""The GearIterator in a generator form."""
    
    # ~ async def generate(self, symbol_list: List[str], min_length: int = 0, max_length: int = 0, init_value: str = "") -> Generator[str]:
        # ~ async for gear_value in GearIterator(symbol_list, min_length, max_length, init_value):
            # ~ async with asyncio.Lock():
                # ~ yield gear_value

# We can then create one instance of the asyncio.Lock shared among the coroutines.
# This can be achieved in the main() coroutine, used as the entry point to the program.
# We can then create a large number of coroutines and pass the shared lock. 
# Each coroutine will have a unique integer argument and a random 
# floating point value between 0 and 1, which will be how long the coroutine will sleep while holding the lock.

# The coroutines are created in a list comprehension and provided to the 
# asyncio.gather() function. The main() coroutine will then block until all coroutines are complete.


