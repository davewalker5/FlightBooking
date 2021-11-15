Airline Booking  System
=======================

A tutorial/demonstration project implementing a Python console application for creating and managing airline flight
bookings and passengers.

The project was inspired by an example in the "Core Python : Getting Started" PluralSight course by Austin Bingham
and Robert Smallshire and is intended as a practice project for the techniques contained in the PluralSight
"Core Python" path.

Structure
=========

+----------------------------+-------------------------------+------------------------------------------------------------------+
| **Project Folder**         | **Package**                   | **Contents**                                                     |
+----------------------------+-------------------------------+------------------------------------------------------------------+
| FlightBooking              | flight_booking                | Classes and business logic for the booking system                |
+----------------------------+-------------------------------+------------------------------------------------------------------+
| FlightBooking              | booking_app                   | Simple console application built over the flight_booking package |
+----------------------------+-------------------------------+------------------------------------------------------------------+
| FlightBookingHtmlGenerator | flight_booking_html_generator | HTML boarding card generator plugin                              |
+----------------------------+-------------------------------+------------------------------------------------------------------+
| FlightBookingPdfGenerator  | flight_booking_pdf_generator  | PDF boarding card generator plugin                               |
+----------------------------+-------------------------------+------------------------------------------------------------------+

Each project contains its own README with further details.

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