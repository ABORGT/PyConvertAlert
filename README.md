# PyConvertAlert

PyConvertAlert makes it easy to take an arbitrary alert from some kind of alerting system (Uptime Robot, Rackspace Intelligence) and convert it into an Alert Manager (Prometheus) alert.


### Getting Started

The latest stable release is available from PyPI:

```
pip install pyconvertalert
```

Otherwise you can install from git:

```
pip install git+https://github.com/jpavlav/PyConvertAlert
```

### Usage

```python
>>> from pyconvertalert import Converter
>>>
>>> test_lookup_dict_1 = {
...     "values": [
...         {
...             "people": [
...                 {
...                     "email": "jim@jim.com",
...                     "phone": "111-111-1111"
...                 }
...             ]
...         }
...     ]
... }
>>>
>>>
>>> test_mapper_dict_1 = {
...     "labels": {
...         "email_address": "email",
...         "phone_number": "phone"
...     }
... }
>>> convert = Converter(mapper=test_mapper_dict_1)
>>> convert.convert_it(test_lookup_dict_1)
{'labels': {'email_address': 'jim@jim.com', 'phone_number': '111-111-1111'}}
```

### Further Usage
In some cases, there will be more than one key that matches a lookup. In this
case, the value returned in our converted dict will be a list containing all of
the values that match this key. In order to handle a situation where we need to
be more specific, it is possible to specify a list of keys to drill down on a
specific value. Here is an example:

```python
>>> test_lookup_dict_2 = {
...     "flowers": [
...         {
...             "best_flower": {
...                 "name": "Orchid",
...                 "scientific_name": "Orchidaceae"
...             },
...             "wild_flower": {
...                 "name": "Gold Yarrow",
...                 "scientific_name": "Achillea filipendulinaa"
...             }
...         }
...     ]
... }
>>>
>>> test_mapper_dict_2 = {
...     "labels": {
...         "best_flower_name": ['best_flower', 'name'],
...         "best_flower_scientific_name": ['best_flower',
...                                         'scientific_name']
...     }
... }
>>>
>>>
>>> convert = Converter(mapper=test_mapper_dict_2)
>>> convert.convert_it(test_lookup_dict_2)
{'labels': {'best_flower_name': 'Orchid', 'best_flower_scientific_name': 'Orchidaceae'}}
```
Above, we see that we were able to get the 'best_flower' 'scientific_name' by
specifying a list of keys to search through. We first return the value from the key 'best_flower', then return the value from the key 'name'.
## Running the tests

Should be as simple as:

```
python -m unittest test_py_convert_alert.py
```

## Contributing
1. Fork it.
2. Create a branch describing either the issue or feature you're working.
3. Making changes, committing along the way.
4. Follow PEP8, except where ridiculous.
5. Include tests for any functionality changes.
6. Push the changes and create a pull request :D.

## Built With

* [Python3](https://www.python.org/downloads/) - Beautiful language.

## Authors

* **Justin Palmer** - *Urrverything* - [Me](https://github.com/jpavlav)

## Acknowledgments

* Kenneth Reitz -> [setup](https://github.com/kennethreitz/setup.py) - Thanks!
* Kamori -> [Cool Guy](https://github.com/Kamori) - Thanks to you as well!
