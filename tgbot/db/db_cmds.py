from typing import List

from tgbot.db.models import Phone, Admin


async def get_models() -> List[Phone]:
    return await Phone.query.distinct(Phone.model).gino.all()


async def get_phones(model) -> List[Phone]:
    return await Phone.query.where(Phone.model == model).gino.all()


async def get_params(name) -> List[Phone]:
    return await Phone.query.where(Phone.name == name).gino.first()


async def get_admins() -> List:
    res = await Admin.query.gino.all()
    admins = []
    for i in res:
        admins.append(i.tg_id)
    return admins


async def add_admins(admin_id, m=None, typ=True):
    try:
        await Admin.create(tg_id=admin_id)
        if typ:
            await m.answer("Admin qo'shildi ✅")
            return True
    except:
        if typ:
            await m.answer("Bu admin mavjud ❌")
            return False


async def add_or_update(**kwargs) -> None:
    phone = await Phone.query.where(Phone.name == kwargs["name"]).gino.first()
    if phone is not None:
        await phone.update(model=kwargs["model"], color=kwargs["color"], month_3=kwargs["month_3"],
                           month_4=kwargs["month_4"], month_6=kwargs["month_6"],
                           month_8=kwargs["month_8"], month_12=kwargs["month_12"], minimum=kwargs["minimum"]).apply()
    else:
        await Phone.create(name=kwargs["name"], model=kwargs["model"], color=kwargs["color"],
                           month_3=kwargs["month_3"], month_4=kwargs["month_4"], month_6=kwargs["month_6"],
                           month_8=kwargs["month_8"], month_12=kwargs["month_12"], minimum=kwargs["minimum"])
