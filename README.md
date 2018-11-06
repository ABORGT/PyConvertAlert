# PyConvertAlert

PyConvertAlert makes it easy to take an arbitrary alert from some kind of alerting system (Uptime Robot, Rackspace Intelligence) and convert it into an Alert Manager (Prometheus) alert.


### Getting Started

The latest stable release is available from PyPi:

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
>>> {'labels': {'email_address': 'jim@jim.com', 'phone_number': '111-111-1111'}}
```
## Running the tests

Should be as simple as:

```
python -m unittest test_py_convert_alert.py
```

## Built With

* [Python3](https://www.python.org/downloads/) - Beautiful language.

## Authors

* **Justin Palmer** - *Urrverything* - [Me](https://github.com/jpavlav)

## Acknowledgments

* Kenneth Reitz -> [setup](https://github.com/kennethreitz/setup.py) - Thanks!
* Kamori -> [Cool Guy](https://github.com/Kamori) - Thanks to you as well!
