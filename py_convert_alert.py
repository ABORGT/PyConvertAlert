#!/usr/bin/env python3
# -*_ coding: utf-8 -*-
#
"""
Simple library to convert an alert from an arbitrary alerting system to an
Alert Manager alert based on config.
"""

import json
import pathlib
import copy
from nested_lookup import nested_lookup, get_occurrence_of_key


class MissingLabelsKey(Exception):
    """
    Simple custom exception in case mapper doesn't meet minimum requirements.

    We want to raise this error if the mapper attribute has no 'labels' key.
    In order to POST an alert to alert manager, there at least must be a
    'labels' key definition.


    """

    pass


class Converter(object):
    """
    Library to easily convert alerts into Alert Manager compatible alerts.

    Alert Manager comes packaged with Prometheus and is a very useful system
    for tracking alerts. Alert rules are typically defined and when that
    criteria is met, Alert Manager receives an alert from Prometheus. What if
    your system utilizes multiple alerting systems, like Rackspace Intelligence
    or Uptime Robot? These too can be pushed to Alert Manager. This lib aims to
    make that conversion as simple as possible.

    """

    def __init__(self, mapper=None):
        """
        Init method.

        mapper : dict or json
            (Default value = None)
            mapper is utilized to search for keys in the originating alert and
            map or assign the values found to the appropriate key in the
            resultant Alert Manager Alert object. The mapper should be a dict
            or json and can be passed either directly, or as a file.

        """
        self.mapper = mapper

    def _check_for_labels(self):
        """
        Return True if 'labels' key defined in self.mapper.

        Here, we ensure that the mapper object has the minimal structure
        required by Alert Manager.

        Returns
        -------
        check : boolean
            check returns true or false after verifying whether or not the
            'labels' key exists in the user provided mapper. Alert manager
            alerts expect at least a labels key in order to POST.

        """
        check = True
        if 'labels' not in self.mapper:
            check = False
        return check

    @property
    def mapping(self):
        """
        Get our mapper object or looks for file containing map.

        This property allows a bit of flexibility with how we specify our
        mapper. If the mapper is provided during instantiation, we roll with
        it. If not, we assume our savvy user is attempting to utilize a json
        config file to attempt the mapping (smart) and try to return the json
        from that file instead.

        Returns
        -------
        self.mapper : str
            Json string representing our alert mapping.


        Raises
        ------
        TypeError
            Raised if the mapper attribute is not a dict.

        MissingLabelsKey
            Raised if the mapper attribute does not contain the key 'labels'.


        """
        try:
            mapper_file = pathlib.Path(self.mapper)
            if mapper_file.is_file():
                with open(self.mapper, 'r') as f:
                    self.mapper = json.load(f)
        except (OSError, TypeError):
            pass
        if not isinstance(self.mapper, dict):
            raise TypeError(f"mapper must be dict {self.mapper} ==> "
                            f"{type(self.mapper)}")
        if not self._check_for_labels():
            raise(MissingLabelsKey(f"mapper must contain 'labels' key at "
                                   f"outer most level: {self.mapper}"))
        return self.mapper

    def _verify_key_exists(self, key, lookup_dict):
        """
        Return True if the specified key exists in our lookup_dict.

        This is a protected method and should not be used outside of the public
        convert_it method. This method is responsible for checking to see if we
        get a hit on a specified key in a lookup on our dict. This helps us
        ensure that during conversion, if any labels annotations or otherwise
        will be unaffected by the conversion and thusly not return empty lists.

        Parameters
        ----------
        key : str
            The key we are looking up in lookup_dict.

        lookup_dict : str
            The lookup_dict is in our case an alert from an arbitrary alerting
            system to be converted to an alert that Alert manager will accept.


        Returns
        -------
        exists : boolean
            Simple flag, True or False, to let us know if our search was
            successful.


        """
        exists = False
        if get_occurrence_of_key(lookup_dict, key) > 0:
            exists = True
        return exists

    def _key_list_search(self, keys_list, lookup_dict):
        """
        Return the final value returned after iterating over keys_list.

        In order to handle situations where a key might exist twice in the
        alert on which we run our lookup, we can specify a list of keys to
        iterate over. Essentially, if a list is provided as the value to one of
        our corresponding alert manager alert keys, we will search for the
        first key in the list, return it's value, then search for the next key
        etc. Finally when we reach the end of our list, the value returned
        should be the result of all searches. This is a protected method and
        should only be used in the public convert_it method.

        Parameters
        ----------
        keys_list : list of str
            This is the list of keys to drill down on. It will be iterated over
            until we reach the end of the list, providing the more specific key
            lookup to prevent multiple values for a single lookup.

        lookup_dict : dict
            This is the arbitrary alert that we are searching through for keys
            to add to our alert manager alert.


        Returns
        -------
        value : str
            This value should be the result of all of the searches for the keys
            provided.

        """
        for index, key in enumerate(keys_list):
            result = nested_lookup(key, lookup_dict)
            try:
                value = nested_lookup(keys_list[index + 1], result)
            except IndexError:
                pass
        return value

    def _add_found_values(self, transform_dict, transform_key,
                          lookup_key, lookup_dict):
        """
        Set value for the specified key in our transform dict to our lookup.

        This is a protected method that shouldn't be used outside of the
        public convert_it method. This method is responsible for all of our
        lookups and assigning the corresponding found value to the appropriate
        key in our alert manager alert.

        Parameters
        ----------
        transform_dict : dict
            The transform_dict is our self.mapping values. The dict is
            transformed by the iterating over it in the convert_it method and
            adding values here.

        transform_key : str
            This is the key we want to target in our transform dict. Ultimately
            the value returne from the lookup will be assigned as the value of
            this key.

        lookup_key : str
            This is the key we are looking up in our arbitrary alert json
            structure to be assigned as the value of the transform_key.

        lookup_dict : dict
            This is the arbitrary alert we are searching for values to be
            assigned to our transform_dict.


        Returns
        -------
        transform_dict : dict
            Return the modified transform dict back to the convert_it method.
            This transform dict should now have the keys we specified in our
            mapper. There corresponding values should now be changed to the
            result of searching for what was the key's previous value (our
            lookup_key is replaced by an actual value).

        """
        try:
            if self._verify_key_exists(lookup_key, lookup_dict):
                transform_dict[transform_key] = \
                    ''.join(nested_lookup(lookup_key, lookup_dict))
        except TypeError:
            pass
        if isinstance(lookup_key, list):
            transform_dict[transform_key] = \
                ''.join(self._key_list_search(lookup_key, lookup_dict))
        return transform_dict

    def _map_to_mapper(self, convert_alert, alert):
        for key, value in convert_alert.items():
            if isinstance(value, dict):
                for k, v in value.items():
                    value = self._add_found_values(value, k, v, alert)
        return value

    def convert_it(self, alert):
        """
        Return either a single converted alert or a list of them.

        This method is responsible for returning our converted alerts. For
        flexibility purposes, it will accept either a single arbitrary alert
        or a list of alerts. If a single alert is provided, a single converted
        alert will be returned. If a list of alerts are provided, a list of
        converted alerts will be returned.

        Parameters
        ----------
        alert : dict
            alert is the alert originating from any arbitrary alerting system.


        Returns
        -------
        ret : dict or list of dicts
            ret is set dynamically based on whether or not a list of dicts is
            passed to convert_it or a single dictionary. Either way, it returns
            a dict where all keys that matched a corresponding key in the
            alert.


        """
        converted_alert = copy.deepcopy(self.mapping)
        converted_alert_list = list()

        if isinstance(alert, list):
            for single_alert in alert:
                converted_alert = copy.deepcopy(self.mapping)
                self._map_to_mapper(converted_alert, single_alert)
                converted_alert_list.append(converted_alert)
            ret = converted_alert_list
        else:
            self._map_to_mapper(converted_alert, alert)
            ret = converted_alert
        return ret
