import peewee
from .auth import db


class BaseModel(peewee.Model):
    id = peewee.PrimaryKeyField(unique=True)

    class Meta:
        database = db


class User(BaseModel):
    telegram_id = peewee.IntegerField(unique=True)

    class Meta:
        db_table = 'users'


class Chanel(BaseModel):
    telegram_id = peewee.IntegerField(unique=True)
    name = peewee.CharField()
    url = peewee.TextField()

    class Meta:
        db_table = 'chanels'


class Referal(BaseModel):
    referal_code = peewee.TextField()
    joined_user = peewee.IntegerField()

    class Meta:
        db_table = 'referals'


class RefCode(BaseModel):
    code = peewee.TextField()
    message = peewee.TextField(default=None, null=True)

    class Meta:
        db_table = 'ref_codes'