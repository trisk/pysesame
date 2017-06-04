pysesame
========

Python API for controlling `Sesame <https://candyhouse.co/>`_ smart locks made
by CANDY HOUSE, Inc. 

This is based on the `cloud API <https://docs.candyhouse.co>`_ for Sesame.

Requirements
------------
Your Sesame needs to be paired with the mobile app in *virtual station*
mode, or a standalone `Wi-Fi Access Point
<https://candyhouse.co/products/wi-fi-access-point>`_.

Dependencies
------------
pysesame depends on the Python package, requests. You can install dependencies
using ``pip install -r requirements.txt``

Usage
-----

.. code:: python

    >> import pysesame

    >> sesames = pysesame.get_sesames("abc@i-lovecandyhouse.co",
                                      "super-strong-password")
    >> [s.nickname for s in sesames]
    ['Front Door', 'Back Door']

    >> front_door = next(s for s in sesames if s.nickname == "Front Door")
    >> front_door.device_id
    'FEEDFACE1234'
    >> front_door.api_enabled
    True
    >> front_door.is_unlocked
    False
    >> front.door.unlock()
    True
    >> front_door.is_unlocked
    True
    >> front.door.is_unlocked = False
    >> front_door.is_unlocked
    False

License
-------
pysesame is released under the MIT license.

