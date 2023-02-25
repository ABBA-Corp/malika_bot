from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.db.db_cmds import get_models, get_phones, get_params


async def model_btns():
    model_btn = InlineKeyboardMarkup(row_width=1)
    res = await get_models()
    for i in res:
        model_btn.add(InlineKeyboardButton(i.model, callback_data=i.model))
    return model_btn


async def phone_btns(model):
    phone_btn = InlineKeyboardMarkup(row_width=1)
    res = await get_phones(model)
    for i in res:
        phone_btn.add(InlineKeyboardButton(i.name, callback_data=i.name))
    phone_btn.add(InlineKeyboardButton("Orqaga 🔙", callback_data="back"))
    return phone_btn


async def params_btns(name, s):
    param_btn = InlineKeyboardMarkup(row_width=1)
    res = await get_params(name)
    arr = res.color.split(', ')
    await s.update_data(month_3=round(float(res.month_3)), month_4=round(float(res.month_4)),
                        month_6=round(float(res.month_6)), month_8=round(float(res.month_8)),
                        month_12=round(float(res.month_12)), min=round(float(res.minimum)))
    for d in arr:
        param_btn.add(InlineKeyboardButton(d, callback_data=d))
    param_btn.add(InlineKeyboardButton("Orqaga 🔙", callback_data="back"))
    return param_btn


async def admin_conf_btn(order_id):
    btns = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('✅ Qabul qilish', callback_data=f"co{order_id}"),
                                                 InlineKeyboardButton('❌ Bekor qilish', callback_data=f"ca{order_id}"),)
    return btns

month_btn = InlineKeyboardMarkup(row_width=1)
month_btn.add(InlineKeyboardButton("3 oylik xarid", callback_data='3'))
month_btn.add(InlineKeyboardButton("4 oylik xarid", callback_data='4'))
month_btn.add(InlineKeyboardButton("6 oylik xarid", callback_data='6'))
month_btn.add(InlineKeyboardButton("8 oylik xarid", callback_data='8'))
month_btn.add(InlineKeyboardButton("12 oylik xarid", callback_data='12'))
month_btn.add(InlineKeyboardButton("Orqaga 🔙", callback_data="back"))

conf_btn = InlineKeyboardMarkup(row_width=1)
conf_btn.add(InlineKeyboardButton("Qabul qilaman ✅", callback_data="confirm"))
conf_btn.add(InlineKeyboardButton("Orqaga 🔙", callback_data="back"))

back_btn = InlineKeyboardMarkup().add(InlineKeyboardButton("Orqaga 🔙", callback_data="back"))

