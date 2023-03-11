from typing import List

from tgbot.db.models import Phone, Admin, Order


async def get_models() -> List[Phone]:
    return await Phone.query.distinct(Phone.model).gino.all()


async def get_phones(model) -> List[Phone]:
    return await Phone.query.where(Phone.model == model).gino.all()


async def get_params(name) -> List[Phone]:
    return await Phone.query.where(Phone.name == name).gino.first()


async def get_list_phones() -> List[Phone]:
    return await Phone.query.gino.all()


async def get_admins() -> List:
    res = await Admin.query.gino.all()
    admins = []
    for i in res:
        admins.append(i.tg_id)
    return admins


async def add_admins(admin_id, m=None, typ=True) -> bool:
    try:
        await Admin.create(tg_id=admin_id)
        if typ:
            await m.answer("Admin qo'shildi ✅")
            return True
    except:
        if typ:
            await m.answer("Bu admin mavjud ❌")
            return False


async def add_order(**kwargs) -> Order:
    new_order = await Order.create(name=kwargs["name"], number=kwargs["number"], passport=kwargs["passport"],
                                   selfie=kwargs["selfie"], card=kwargs["card"], time=kwargs["time"],
                                   model=kwargs["model"], phone=kwargs["phone"], color=kwargs["color"],
                                   type=kwargs["type"], status=kwargs["status"])
    return new_order


async def update_order(**kwargs) -> int:
    order = await Order.query.where(Order.id == kwargs["id"]).gino.first()
    if kwargs["file"] is None:
        await order.update(status=kwargs["status"]).apply()
    else:
        await order.update(file=kwargs["file"]).apply()
    return order.id


async def get_order(**kwargs) -> Order:
    order = await Order.query.where(Order.id == kwargs["id"]).gino.first()
    return order


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

