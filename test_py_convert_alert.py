import unittest


from py_convert_alert import Converter


class TestConvertIt(unittest.TestCase):
    """Test case for Convert it's only public method."""

    def test_convert_it_1(self):
        """Test that convert it produces the desired dict."""
        test_lookup_dict_1 = {
            "values": [
                {
                    "people": [
                        {
                            "email": "jim@jim.com",
                            "phone": "111-111-1111"
                        }
                    ]
                }
            ]
        }

        test_mapper_dict_1 = {
            "labels": {
                "email_address": "email",
                "phone_number": "phone"
            }
        }

        convert = Converter(mapper=test_mapper_dict_1)
        converted = convert.convert_it(test_lookup_dict_1)
        check_converted = {
            'labels': {
                'email_address': 'jim@jim.com',
                'phone_number': '111-111-1111'
            }
        }
        self.assertEqual(converted, check_converted)

    def test_convert_it_2(self):
        """
        Test that convert it produces the desired dict with list.

        This test differs from the above because we are searching for a key
        that exists more than once in our lookup_dict. In order to get the
        correct value out of that search, we set the value of the key in our
        mapper to a list of keys. The list of keys is iterated over, returning
        each subsequent result until the specified key/value in our lookup_dict
        is found and returned.


        """
        test_lookup_dict_2 = {
            "flowers": [
                {
                    "best_flower": {
                        "name": "Orchid",
                        "scientific_name": "Orchidaceae"
                    },
                    "wild_flower": {
                        "name": "Gold Yarrow",
                        "scientific_name": "Achillea filipendulinaa"
                    }
                }
            ]
        }

        test_mapper_dict_2 = {
            "labels": {
                "best_flower_name": ['best_flower', 'name'],
                "best_flower_scientific_name": ['best_flower',
                                                'scientific_name']
            }
        }

        convert = Converter(mapper=test_mapper_dict_2)
        converted_2 = convert.convert_it(test_lookup_dict_2)
        check_converted_2 = {
            'labels': {
                'best_flower_name': 'Orchid',
                'best_flower_scientific_name': 'Orchidaceae'
            }
        }
        self.assertEqual(converted_2, check_converted_2)


if __name__ == '__main__':
    unittest.main()
