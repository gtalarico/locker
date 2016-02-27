class Locker(object):

    def __init__(self, capacity):
        print 'Locker Initialized.'
        self.chambers = []
        self.chambers = [Chamber(n) for n in range(capacity)]
        print 'Locker Created: ', self

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


class Chamber(object):

    def __init__(self, uid):
        self.uid = uid
        self.user = None
        print 'Chamber Initialized: ', self

    @property
    def occupied(self):
        return bool(self.user)

    @property
    def available(self):
        return not self.occupied

    def reserve(self, user):
        self.user = user
        print 'Chamber Reserved: ', self

    def release(self):
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
            chamber.reserve(User(pin))
        else:
            print 'Chambers Full. Wait for relase.'
    print 'New Status: ', locker
