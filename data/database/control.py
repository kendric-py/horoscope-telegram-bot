import peewee
from .auth import db
from .models import (
    User, Chanel, Referal
)


db.create_tables([User, Chanel, Referal])

async def create_user(user_id: int) -> User:
    try:
        user = User.create(
            telegram_id = user_id
        )
        return(user)
    except peewee.IntegrityError:
        return


async def get_user(user_id: int) -> User:
    try:
        user = User.get(User.telegram_id == user_id)
    except User.DoesNotExist:
        user = None
    return(user)


async def get_users() -> list:
    users = User.select()
    return(users)


async def get_count_users() -> int:
    count = User.select().count()
    return(count)


async def delete_user(user_id: int) -> None:
    User.delete().where(User.telegram_id == user_id)
    return


async def get_chanels():
    chanels = Chanel.select()
    return(chanels)