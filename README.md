## Virtual Python Locker

A simple locker controller application.

The idea is too simulate a real work locker, where access is granted (open + release) after a unique PIN is entered.

The unique PIN could be created manually through a keypad, or through an interface such as
a MAG strip reader, NFC reader, Fingerprint, etc.

The current application checks if it can talk with a Raspberry Pi, and wait for a signal from Raspberry PI's RPio.
If it fails, it falls back to the host's keyboard for user input.


[Peewee](http://docs.peewee-orm.com/) was used as an ORM to simplify relantionship with SQLite database.


#### Use

> python locker.py

1. Enter a Unique PIN.
2. A virtual locker is reserved.
3. Enter a new unique PIN.
4. If it matches one of the current lockers, it releases.
5. If it does not match, a new locker is reserved under the new pin.
6. Type pin 1111 to clear all lockers
