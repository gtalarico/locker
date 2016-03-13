from peewee import SqliteDatabase, Model
from peewee import CharField, IntegerField, ForeignKeyField, BooleanField
from peewee import DateTimeField
from peewee import OperationalError, IntegrityError
from playhouse.hybrid import hybrid_property

from datetime import datetime
import os

path = os.path.dirname(__file__)
db = SqliteDatabase(os.path.join(path,'locker.db'))
db.connect()

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    pin = CharField(primary_key=True)
    active = BooleanField(default = False)

    def __repr__(self):
        return '<USER> PIN:{}'.format(self.pin)

    @db.atomic()
    def set_active(self, status):
        self.active = status
        self.save()

    @staticmethod
    @db.atomic()
    def create_user(pin):
        user, was_created = User.create_or_get(pin=pin)
        if was_created:
            user.save()
        return user




class Chamber(BaseModel):
    chamber_id = IntegerField(primary_key=True)
    user = ForeignKeyField(User, related_name="chambers", null=True)
    status = CharField(default='virgin')

    @hybrid_property
    def occupied(self):
        return bool(self.user)

    @hybrid_property
    def available(self):
        return not self.occupied

    def reserve(self, user):
        user.set_active(True)
        self.user = user
        self.status = 'reserved'
        self.save()

        print('Chamber Reserved: ', self)
        op = Operation.add_operation(chamber=self, user=user,
                                     action='reserved')

    def release(self):
        self.user.set_active(False)
        self.user = None
        self.status = 'available'
        self.save()

        print('Chamber Released: ', self)
        op = Operation.add_operation(chamber=self, action='released')

    def __repr__(self):
        return '<CHAMBER {}:{}>:{}:{}'.format(self.chamber_id, self.occupied,
                                              self.status, self.user )

    @staticmethod
    @db.atomic()
    def get_or_create_chamber(chamber_id):
        chamber, was_created = Chamber.get_or_create(chamber_id=chamber_id)
        if was_created:
            chamber.save()
        return chamber


class Operation(BaseModel):
    timestamp = DateTimeField(primary_key=True)
    user = ForeignKeyField(User, related_name="operations", null=True)
    chamber = ForeignKeyField(Chamber, related_name='chamber', null=True)
    action = CharField(null=True)
    locker = CharField(default='Dev Locker')

    def __repr__(self):
        return '<TRANSACTION> {}'.format(self.timestamp)

    @staticmethod
    @db.atomic()
    def add_operation(chamber=None, action=None, user=None):
        now = datetime.utcnow()
        op = Operation.create(timestamp=now, chamber=chamber,
                              action=action, user=user)
        op.save()
        return op

# this creates indexes, not sure why
tables = [User, Operation, Chamber]
db.create_tables(tables, True)

# ERASE TABLES
def drop_tables():
    try:
        db.drop_tables(tables)
    except:
        pass
