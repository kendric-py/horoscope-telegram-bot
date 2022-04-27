import peewee
from .auth import db
from .models import (
    User, Chanel, Referal, RefCode
)


db.create_tables([User, Chanel, Referal, RefCode])

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
    User.delete().where(User.telegram_id == user_id).execute()
    return


async def get_chanels():
    chanels = Chanel.select()
    return(chanels)


async def new_chanel(name: str, link: str, telegram_id: int) -> Chanel:
    chanel = Chanel.create(
        telegram_id=telegram_id,
        name=name,
        url=link
    )
    return(chanel)


async def delete_chanel(chanel_id: int) -> None:
    Chanel.delete().where(Chanel.id == chanel_id).execute()
    return


async def create_ref_code(ref_code: str, message: str) -> RefCode:
    code = RefCode.create(
        code = ref_code,
        message = message
    )
    return(code)



async def get_count_use_referal_code(ref_code: str) -> int:
    count = Referal.select().where(Referal.referal_code == ref_code).count()
    return(count)


async def search_referal_code(ref_code: str) -> RefCode:
    try:
        code = RefCode.get(RefCode.code == ref_code)
    except RefCode.DoesNotExist:
        code = None
    return(code)
