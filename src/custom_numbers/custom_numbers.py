r"""NAME
    custom_numbers

MODULE REFERENCE
    N/A

DESCRIPTION
    Swiss-army knife for custom numeral systems.
    
    Copyright (c) 2023 Evgueni Antonov. All rights reserved.
    This work is licensed under the terms of the MIT license.
    See LICENSE file or https://mit-license.org/

CLASSES
    CustomNumeralSystem
    CustomNumber
    GearIterator
"""

import re
from typing import List, Generator
import threading
import asyncio
import multiprocessing as mp
from ctypes import c_wtypes_p

# https://www.reddit.com/r/learnmath/comments/13v410v/what_common_known_symbols_a_numeral_system_with/

class CustomNumeralSystem:
    r"""Definition of custom numeral systems with basic consistency validation.
    
    Args:
        symbols: String of symbols to be perceived as digits.
                The symbol order is important: 'smallest' is first on the left!
                This string length would be the numeral system base.
                Obviously each "digit" would consist of a single-
                character.
    
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
    
    
    def __init__(self, symbols: str) -> None:
        self._digits: List[str] = [c for c in symbols]
        self._base: int = len(symbols)
        
        if len(symbols) == 0:
            raise ValueError("Empty 'symbols' argument given.")
        
        if len(symbols) != len(set(self._digits)):
            raise ValueError("Duplicate symbols in the 'symbols' argument.")
        
        # I don't need we need to put a limit here. Let the user decide.
        #if self._base > self._MAXBASE:
        #    raise ValueError(f"Unsupported numeral base given {self._base}. Maximum base supported is {self._MAXBASE}.")
        
    
    def __repr__(self) -> str:
        return "".join(self._digits)
    
    
    @property
    def sign_support(self) -> bool:
        return self._SIGNSUPPORT
    
    
    @property
    def symbol_list(self) -> List[str]:
        return self._digits.copy()
    
    

class CustomNumber:
    r"""Definition of a number from the CustomNumericalSystem."""
    
    def __init__(self, numeral_system: CustomNumeralSystem, init_value: str = "", init_value_int: int = 0) -> None:
        self._numeral_system: CustomNumeralSystem = numeral_system
        #self._symbol_list: List[str] = numeral_system.symbol_list
        self._init_value: str = init_value # Just in case we will keep the original value
        self._value: str = self._init_value
        
        # Validation: Is this digit belonging to this numeral system?
        regex_str = re.sub(r"[\s,']", "", str(symbol_list))
        regex_str = re.sub(r"\[", "[^", regex_str)
        regex = re.compile(regex_str)
        if regex.search(init_value):
            raise ValueError("Incorrect symbols in init_value, which are not in the 'symbols' argument.")
    
    
    def __repr__(self) -> str:
        return self._value
    
    
    @property
    def init_value(self) -> str:
        return self._init_value
    
    
    def to_int(self) -> int:
        return int(self._value)
    
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
    
    def __init__(self, symbols: str, min_length: int = 0, max_length: int = 0, init_value: str = "") -> None:
        numeral_system: object = CustomNumeralSystem(symbols)
        self._symbol_list: List[str] = numeral_system.symbol_list
        self._init_value: str = init_value
        
        
        
        
        
        if len(symbol_list) == 0:
            raise ValueError("Empty symbol_list given.")
        
        if len(symbol_list) != len(set(symbol_list)):
            raise ValueError("Duplicate symbols in the symbol_list.")
        
        if max_length > 0 and min_length > max_length:
            raise ValueError("min_length is greather than max_length.")
        
        if len(init_value) > 0 and (len(init_value) < min_length or (max_length > 0 and len(init_value) > max_length)):
            raise ValueError("Incorrect init_value length.")
        
        regex_str = re.sub(r"[\s,']", "", str(symbol_list))
        regex_str = re.sub(r"\[", "[^", regex_str)
        regex = re.compile(regex_str)
        if regex.search(init_value):
            raise ValueError("Incorrect symbols in init_value, which are not in the symbols_list.")
        
        self._init_value_returned: bool = False
        self._index: int = 0
        self._symbol_list: List[str] = symbol_list.copy()
        self._min_length = min_length
        self._max_length = max_length
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
        # Critical section
        with threading.Lock():
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
        
        Not sure we will need this, but it's there"""
        return self
    
    
    def __exit__(self, exc_type, exc_value, exc_tb) -> bool:
        r"""Context management protocol.
        
        StopIteration exception will not be propagated.
        
        Not sure we will need this, but it's there"""
        return True # We won't propagate the StopIteration exception




class GearGenerator:
    r"""The GearIterator in a generator form."""
    
    def generate(self, symbol_list: List[str], min_length: int = 0, max_length: int = 0, init_value: str = "") -> Generator[str]:
        for gear_value in GearIterator(symbol_list, min_length, max_length, init_value):
            with asyncio.Lock():
                yield gear_value


class AsyncGearGenerator:
    r"""The GearIterator in a generator form."""
    
    async def generate(self, symbol_list: List[str], min_length: int = 0, max_length: int = 0, init_value: str = "") -> Generator[str]:
        async for gear_value in GearIterator(symbol_list, min_length, max_length, init_value):
            async with asyncio.Lock():
                yield gear_value

# We can then create one instance of the asyncio.Lock shared among the coroutines.
# This can be achieved in the main() coroutine, used as the entry point to the program.
# We can then create a large number of coroutines and pass the shared lock. 
# Each coroutine will have a unique integer argument and a random 
# floating point value between 0 and 1, which will be how long the coroutine will sleep while holding the lock.

# The coroutines are created in a list comprehension and provided to the 
# asyncio.gather() function. The main() coroutine will then block until all coroutines are complete.


