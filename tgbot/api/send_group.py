from aiogram import types
from aiogram.types import InputFile

from tgbot.keyboards.inline import admin_conf_btn


async def group(order, names, bot, config):
    media = types.MediaGroup()
    media.attach_photo(InputFile("awdaw.jpg"))
    media.attach_photo(InputFile("awdaw.jpg"), caption=f"🆔 So'rov id: {order.id}\n"
                                                    f"👨 Ismi: {order.name}\n"
                                                    f"📞 Telefon raqami: {order.number}\n"
                                                    f"💳 Karta raqami: {order.card}\n"
                                                    f"💳 Karta muddati: {order.time}\n"
                                                    f"📱 Model: {order.phone}\n"
                                                    f"🎨 Rangi: {order.color}\n"
                                                    f"📆 Muddati: {order.type} oy\n")
    await bot.send_media_group(chat_id=config.tg_bot.channel_ids, media=media)
    await bot.send_message(chat_id=config.tg_bot.channel_ids, text="Tasdiqlaysizmi? 👆", reply_markup=await admin_conf_btn(order.id))
