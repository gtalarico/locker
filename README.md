## Python Locker

A simple locker controller application.

The idea is too simulate a real work locker, where access is granted (open and release) after a unique PIN is entered. The PIN could be entered through any interface, and could represent a unique MAG strip data, NFC chip, Fingerprint, or simple keypad pin.

The current application check if it can talk with a raspberry pi to get a PIN from a keyboard. If it fails, it falls back to the hosts' keyboard for tests.

### Use

> python locker.py

* Enter a Unique PIN.
* a virtual locker is reserved.
* Enter a new PIN.
* If it matches one of the current lockers, it releases
* If it does not match, a new locker is reserved.

* Type pin 1111 to clear all lockers
