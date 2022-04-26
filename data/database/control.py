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