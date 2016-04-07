import model
from model import Operation, User, Chamber
import sys

try:
    from key import get_pin
except ImportError:
    pi_present = False
else:
    pi_present = True

NUM_CHAMBERS = 4

class Locker(object):

    def __init__(self, capacity):
        print('Locker Initialized.')
        self.chambers = [Chamber.get_or_create_chamber(n) for n in range(capacity)]
        print('Locker Created: ', self)

    @property
    def available_chambers(self):
        return [chamber for chamber in self.chambers if chamber.available]

    @property
    def occupied_chambers(self):
        return [chamber for chamber in self.chambers if chamber.occupied]

    def find_available_chamber(self):
        try:
            return self.available_chambers[0]
        except IndexError:
            return None

    def find_chamber_by_pin(self, pin):
        for chamber in self.occupied_chambers:
            if pin == chamber.user.pin:
                return chamber
        return None

    def count_available(self):
        return len(self.available_chambers)

    def __len__(self):
        return len(self.chambers)

    def __repr__(self):
        return '<LOCKER: {} of {} Available>:'.format(self.count_available(),
                                                      len(self))

locker = Locker(NUM_CHAMBERS)

if __name__ == '__main__':

    # Start locker
    while True:

        if pi_present:
            pin = get_pin(4)
        else:
            pin = raw_input('Locker Idle. Enter Unique PIN:')

        if pin == '1111':
            model.drop_tables()
            sys.exit()

        chamber = locker.find_chamber_by_pin(pin)

        if chamber:
            chamber.release()

        else:
            chamber = locker.find_available_chamber()
            if chamber:
                user = User.create_user(pin)
                chamber.reserve(user)

            else:
                print('Chambers Full. Wait for relase.')

        print('New Status: ', locker)
