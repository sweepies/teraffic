Teraffic
========

This utility provides an easy way of viewing total network traffic since
the last boot.

Installation
------------

* Clone with git and run ``setup.py install``
* Install from PyPI_: ``pip install teraffic``

.. _PyPI: https://pypi.python.org/pypi/Teraffic/


Usage
-----

Usage: 
  teraffic.py <network interface> [options]

Options:
  -h, --help  show this help message and exit
  -r, --raw   don't format the number of bytes
  -i, --in    only show ingress traffic
  -o, --out   only show egress traffic
