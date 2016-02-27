class Locker(object):

    def __init__(self, capacity):
        self.chambers = {}

        print 'Locker Initialized.'
        for n, chamber in enumerate(range(0, capacity)):
            self.chambers[n] = Chamber(n)
        print 'Locker Created: ', self

    def find_chamber_by_pin(self, pin):
        for chamber in self.chambers.values():
            if pin == getattr(chamber.user, 'pin', None):
                return chamber
        return None

    def find_available_chamber(self):
        for chamber in self.chambers.values():
            if chamber.occupied is False:
                return chamber
        return None

    def count_available(self):
        counter = 0
        for chamber in self.chambers.values():
            if chamber.occupied is False:
                counter += 1
        return counter

    def __len__(self):
        return len(self.chambers.keys())

    def __repr__(self):
        return '<LOCKER: {} of {} Available>:'.format(self.count_available(), len(self))


class Chamber(object):

    def __init__(self, uid):
        self.uid = uid
        self.occupied = False
        self.user = None
        print 'Chamber Initialized: ', self

    def reserve(self, user):
        self.occupied = True
        self.user = user
        print 'Chamber Reserved: ', self

    def release(self):
        self.occupied = False
        user = self.user
        del user
        self.user = None

        print 'Chamber Released: ', self

    def __repr__(self):
        return '<CHAMBER {}:{}>:{}'.format(self.uid, self.occupied,
                                             self.user)

class User(object):

    def __init__(self, pin):
        self.pin = pin

        print 'User Created: ', self

    def __repr__(self):
        return '<USER PIN: {}>'.format(self.pin)

locker = Locker(4)

while True:

    pin = raw_input('Locker Idle. Enter Unique PIN:')

    chamber = locker.find_chamber_by_pin(pin)

    if chamber:
        chamber.release()

    else:
        chamber = locker.find_available_chamber()
        if chamber:
            user = User(pin)
            chamber.reserve(user)
        else:
            print 'Chambers Full. Wait for relase.'

    print 'New Status: ', locker
