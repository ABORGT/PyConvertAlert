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
        self._mapper = mapper

    @property
    def mapping(self):
        """Get our mapper object or looks for file containing map.

        This property allows a bit of flexibility with how we specify our
        mapper. If the mapper is provided during instantiation, we roll with
        it. If not, we assume our savvy user is attempting to utilize a json
        config file to attempt the mapping (smart) and try to return the json
        from that file instead.

        Returns
        -------
        self._mapper : str
            Json string representing our alert mapping.


        """
        try:
            mapper_file = pathlib.Path(self._mapper)
            if mapper_file.is_file():
                with open(self._mapper, 'r') as f:
                    self._mapper = json.load(f)
        except (OSError, TypeError):
            pass
        if not isinstance(self._mapper, dict):
            raise TypeError("mapper must be dict {}==>{}".format(self._mapper,
                                                                 type(self._mapper)))
        return self._mapper
