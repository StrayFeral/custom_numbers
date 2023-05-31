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

## USAGE

```
from custom_numbers install custom_numbers as cn

my_custom_numeral_system = cn.CustomNumeralSystem("paf")
my_number = cn.CustomNumber(my_custom_numeral_system, "a")

# Now if you type in REPL:
# help(cn)
# You will get the help for the module and the classes.
```

### NOTE

We could also import in a short way like this

```
import custom_umbers as cn
```

And things would work.

```
my_custom_numeral_system = cn.CustomNumeralSystem("paf")
my_number = cn.CustomNumber(my_custom_numeral_system, "a")
```

However you won't be able to get some extras, as the help for example as
in REPL this would produce the help for the package, not for the module.

```
help(cn)
```
