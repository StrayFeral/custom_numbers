# custom_numbers 0.0.1

## DESCRIPTION

A Swiss-army knife for numbers of custom numeral systems.

## AUTHOR

Evgueni Antonov 2023.

## NOTE

This module was created and tested on Python 3.10.6, pip 23.1.2.

## INSTALLATION

```
pip3 install custom-numbers
# or
python3 -m pip install custom-numbers
```

## QUICKSTART

For details on how to use it, see the USAGE section below.

```
from custom_numbers import custom_numbers as cn

my_custom_numeral_system = cn.CustomNumeralSystem("paf")
my_number = cn.CustomNumber(my_custom_numeral_system, "a")

# Now if you type in REPL:
# help(cn)
# You will get the help for the module and the classes.
```

## USAGE

This package contains one module with few classes made to help you declare
a custom numeral system, made of custom symbols with a custom base. As
this may sound strange, in reality this is how it looks:

> NOTE: Subsystems are not supported and I do not plan to implement this
> feature.

### QUICK RECAP ON EXISTING AND WELL-KNOWN NUMERAL SYSTEMS

Let's start with something you already know - a binary number. These
are made of only **zeroes and ones** and therefore the Base is 2.

> Example: 1100101

and this actually is the title of a really cool song from the 90s.
Also **1100101** binary, converted to decimal is **101** (a hundred and one),
just like (binary) **10<sub>2</sub>** == **2<sub>10</sub>** (decimal).

Now - a hexadecimal number - these are made of the digits
**0, 1, 2, 3, 4, 5, 6, 7, 8, 9** and the letters
**A, B, C, D, E, F** and have a Base of 16.

So a hexadecimal number looks like this:

> F<sub>16</sub> == 15<sub>10</sub>, 
> 10<sub>16</sub> == 16<sub>10</sub>, 
> F0<sub>16</sub> == 240<sub>10</sub>

The other well-known numeral system is the octal system, consisting of
only digits from zero to seven and Base 8, but we will skip this one now.

And finally the decimal system which we all know since childhood have a
Base of 10 and is made of the digits from zero to nine.

### TUTORIAL: DECLARING A CUSTOM NUMERAL SYSTEM

Okay, so far you are familiar with the most widely used numeral system -
the binary, the octal, the decimal and the hexadecimal.

Let's start by re-defining the binary system. So it does have a Base of 2
and we won't change that. However how about instead of using **0 and 1**
to use **P and A** instead? So **P** would be our new zero and **A** would
be our new one. Therefore as we normally would write **1100101** this now
would be written as **AAPPAPA**. Confusing, right? But so what - it is
still a binary system, we just changed the symbols.

But now how about something crazier - a numeral system with a Base of 3,
using the symbols **P, A, F** as digits, so **F** would be **2** decimal,
**P** would be **0** decimal. Therefore:

> AA<sub>3</sub> == 4<sub>10</sub>, 
> AF<sub>3</sub> == 5<sub>10</sub>, 
> FP<sub>3</sub> == 6<sub>10</sub>

Now let's see this in action:

```
from custom_numbers import custom_numbers as cn

sys3 = cn.CustomNumeralSystem("paf")
num3 = cn.CustomNumber(sys3, "aa")
num10 = num3.to_decimal()
print(num10) # Prints "4"
```

Best way to test if the classes work as expected is to declare numeral
systems with the symbols we all know:

```
from custom_numbers import custom_numbers as cn

sys2 = cn.CustomNumeralSystem("01")
num2 = cn.CustomNumber(sys2, "1100101")
num10 = num2.to_decimal()
print(num10) # Prints "101"

sys16 = cn.CustomNumeralSystem("0123456789abcdef")
num16 = cn.CustomNumber(sys16, "f0")
num10 = num16.to_decimal()
print(num10) # Prints "240"
```

So far so good. Now let's go totally nuts and declare a system with a
Base greather than 16 and a totally weird set of symbols for digits.
And we can actually do that and even more totally crazy stuff:

```
sysN = cn.CustomNumeralSystem("kje5nCs21Q9vW0KMqc")
```

> NOTE: The custom numbers are CASE SENSITIVE!!
> So **N != n** !!

> NOTE: There are forbidden characters, which can't be used in a numeral
> system and can't be used in a number. You could always get them as a
> string by using the **forbidden_characters** property of the 
> **CustomNumeralSystem** class.

> NOTE: **CustomNumber** class defines only unsigned "integers"!
> Therefore the plus and minus characters are forbidden.

### class CustomNumeralSystem

Defines and declares a custom numeral system.

```
CustomNumeralSystem(digits: str)

Args:
    digits: The symbols to be used as digits. The string length defines
        the numeral system base.
```

PROPERTIES:

```
sign_support -> bool
forbidden_characters -> str
base -> int
```

METHODS:

```
valid_number(number: str) -> bool
    Tests if the given "number" is valid for the current numeral system.
    Should not contain forbidden characters.
    Should contain only characters defined in the numeral system.
```

### class CustomNumber

Defines and declares a number from a custom numeral system.

```
CustomNumber(numeral_system: CustomNumeralSystem, value: str)

Args:
    numeral_system: A previously defined custom numeral system.
    value: The value (the number itself).
```

PROPERTIES:

```
init_value -> str
    Returns the initial value the class was initialized with.
```

METHODS:

```
digit_to_int(digit: str) -> int
    Converts the given digit from the custom numeral system to a
    decimal integer.

to_decimal() -> int
    Converts the current number value to a decimal integer.
```

### class GearIterator

Iterates over the numbers of a custom numeral system eiter starting at
the very first number (the zero-equivalent) or starting from a given
init_value.

Briefly simulates old gear counters, like the old cars odometer.

```
GearIterator(numeral_system: CustomNumeralSystem, min_length: int = 0, max_length: int = 0, init_value: str = "")

Args:
    numeral_system: Custom numeral system. Mind the order of symbols!
    min_length: Minimum length, default is zero.
    max_length: Maximum length, default is zero - means no limit.
    init_value: Value to initialize with.
```
