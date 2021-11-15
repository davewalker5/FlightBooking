flight_booking_html_generator
=============================
A tutorial/demonstration project implementing a Python plugin for creating boarding card content in HTML format. The
plugin is intended to be used with the "flight_booking" demonstration project.

The boarding card template is taken from the following Codepen by @ramiru, with some modifications:

https://codepen.io/ramiru/pen/oXmyyy

The aircraft image used in the boarding card is from ClipartMax, with some modifications:

https://www.clipartmax.com/middle/m2H7H7m2m2d3H7H7_herbivorous-clipart-airplane-airplane-outline-png/

Overview
========

The flight.py module of the flight_booking project discovers plugins extending the following entry point:

::

    flight_booking.card_generator_plugins

Plugins are expected to provide the following symbols:

+----------------+------------------------------------------------------------------------------------------------------------+
| Symbol         | Comments                                                                                                   |
+================+============================================================================================================+
| card_format    | String containing the supported format e.g. "html"                                                         |
+----------------+------------------------------------------------------------------------------------------------------------+
| card_generator | Callable that receives a dictionary of boarding card details and returns the content for the boarding card |
+----------------+------------------------------------------------------------------------------------------------------------+

Unit Tests
==========

To run the unit tests, a virtual environment should be created, the requirements should be installed using pip and the
environment should be activated.

The tests can then be run from the command line, at the root of the project folder, as follows:

::

    source venv/bin/activate
    python -m unittest

Generating Documentation
========================

To generate the documentation, a virtual environment should be created, the requirements should be installed
using pip and the environment should be activated.

HTML documentation can then be created by running the following command from the "docs" sub-folder:

::

    make html

The resulting documentation is written to the docs/build/html folder and can be viewed by opening "index.html" in a
web browser.

Distribution
============

A distribution can be created by running the following from a command prompt at the root of the project:

::

    python setup.py bdist_wheel

Note that the project's virtual environment should **not** be activated when creating distributions.

License
=======

This software is licensed under the MIT License:

https://opensource.org/licenses/MIT

Copyright 2021 David Walker

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.