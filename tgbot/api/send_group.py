from aiogram import types
from aiogram.types import InputFile

from tgbot.keyboards.inline import admin_conf_btn


async def group(bot, config, **kwargs):
    media = types.MediaGroup()
    media.attach_photo(f"https://malikabackapi.itlink.uz/{kwargs['passport']}")
    media.attach_photo(f"https://malikabackapi.itlink.uz/{kwargs['selfie']}", caption=f"🆔 So'rov id: {kwargs['id']}\n"
                                                    f"👨 Ismi: {kwargs['name']}\n"
                                                    f"📞 Telefon raqami: {kwargs['number']}\n"
                                                    f"💳 Karta raqami: {kwargs['card']}\n"
                                                    f"💳 Karta muddati: {kwargs['time']}\n"
                                                    f"📱 Model: {kwargs['phone']}\n"
                                                    f"🎨 Rangi: {kwargs['color']}\n"
                                                    f"📆 Muddati: {kwargs['type']} oy\n")
    await bot.send_media_group(chat_id=config.tg_bot.channel_ids, media=media)
    await bot.send_message(chat_id=config.tg_bot.channel_ids, text="Tasdiqlaysizmi? 👆",
                           reply_markup=await admin_conf_btn(kwargs['id']))
