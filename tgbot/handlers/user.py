from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, InputFile

from tgbot.filters.back import BackFilter
from tgbot.keyboards.inline import model_btns, phone_btns, params_btns, month_btn, conf_btn
from tgbot.keyboards.reply import contact_btn, remove_btn
from tgbot.misc.states import UserGet


async def user_start(m: Message):
    await m.reply("Assalomu alaykum! 👋\n"
                  "Markab botiga xush kelibsiz\n"
                  "Siz bu yerda tovar xarid qilish uchun birinchi navbata\n"
                  "Ism Familya Sharifingizni kiriting!")
    await UserGet.get_name.set()


async def get_name(m: Message, state: FSMContext):
    await state.update_data(name=m.text)
    await m.answer("Iltimos telefon raqamingizni yuboring! 📱", reply_markup=contact_btn)
    await UserGet.next()


async def get_number(m: Message, state: FSMContext):
    await state.update_data(number=m.contact.phone_number)
    await m.answer("Iltimos passportingizni fotosuratini tashlang 🪪", reply_markup=remove_btn)
    await UserGet.next()


async def get_pass(m: Message, state: FSMContext):
    await state.update_data(pass_id=m.photo[0].file_id)
    await m.answer("Iltimos passportingiz bn selfi qilib tashlang 🤳")
    await UserGet.next()


async def get_self(m: Message, state: FSMContext):
    await state.update_data(self_id=m.photo[0].file_id)
    await m.answer("Iltimos karta raqamin gizni kiriting tekshirib olishimiz uchun. 💳")
    await UserGet.next()


async def get_card(m: Message, state: FSMContext):
    await state.update_data(card=m.text)
    await m.answer("Karta amal qilish muddatini kiriting")
    await UserGet.next()


async def get_time(m: Message, state: FSMContext):
    await state.update_data(time=m.text)
    await m.answer("Modellardan birini tanlang 👇", reply_markup=await model_btns())
    await UserGet.next()


async def get_model(c: CallbackQuery, state: FSMContext):
    await state.update_data(model=c.data)
    await c.message.edit_text(f"{c.data}lardan birini tanlang 👇", reply_markup=await phone_btns(c.data))
    await UserGet.next()


async def get_phone(c: CallbackQuery, state: FSMContext):
    await state.update_data(phone=c.data)
    await c.message.edit_text("Iltimos rangini tanlang 👇", reply_markup=await params_btns(c.data, state))
    await UserGet.next()


async def get_color(c: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.update_data(color=c.data)
    await c.message.edit_text(f"📱 {data['phone']}\n"
                              f"📅 3 oylik to\'lov: {data['month_3']:,} so'm dan\n"
                              f"📅 4 oylik to\'lov: {data['month_4']:,} so'm dan\n"
                              f"📅 6 oylik to\'lov: {data['month_6']:,} so'm dan\n"
                              f"📅 8 oylik to\'lov: {data['month_8']:,} so'm dan\n"
                              f"📅 12 oylik to\'lov: {data['month_12']:,} so'm dan\n"
                              f"💵 Boshlang\'ich to\'lov: {data['min']:,} so'm dan\n"
                              f"🔄 Agar bundan ko'proq to\'lov qilsangiz oylik to\'lovlarga ta\'sir qiladi!",
                              reply_markup=month_btn)
    await UserGet.next()


async def get_type(c: CallbackQuery, state: FSMContext):
    await state.update_data(month=c.data)
    await c.message.delete()
    await c.message.answer_document(InputFile("Согласие.docx"), caption="Iltimos soglasovanieni qabul qiling 👆",
                                    reply_markup=conf_btn)
    await UserGet.next()


async def get_conf(c: CallbackQuery, state: FSMContext):
    config = c.bot.get("config")
    data = await state.get_data()
    media = types.MediaGroup()
    media.attach_photo(data['pass_id'])
    media.attach_photo(data['self_id'], caption=f"👨 Ismi: {data['name']}\n"
                                                f"📞 Telefon raqami: {data['number']}\n"
                                                f"💳 Karta raqami: {data['card']}\n"
                                                f"💳 Karta muddati: {data['time']}\n"
                                                f"📱 Model: {data['model']}\n"
                                                f"🎨 Rangi: {data['color']}\n"
                                                f"📆 Muddati: {data['month']} oy\n")
    for i in config.tg_bot.channel_ids:
        await c.bot.send_media_group(chat_id=i, media=media)
    await c.message.delete()
    await c.message.answer("Raxmat, so'rovingiz qabul qilindi!\n"
                              "Siz bilan tez orada agentimiz bog'lanadi. 👨‍💻\n"
                              "Tanlovingiz uchun raxmat. 😃\n"
                              "Yangi so'rov qoldirish uchun Ism Familya Sharifingizni yuboring!")
    await state.reset_data()
    await UserGet.get_name.set()


async def back(c: CallbackQuery):
    await c.message.delete()
    await c.message.answer("Modellardan birini tanlang 👇", reply_markup=await model_btns())
    await UserGet.get_model.set()


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(get_name, state=UserGet.get_name)
    dp.register_message_handler(get_number, content_types=types.ContentType.CONTACT, state=UserGet.get_number)
    dp.register_message_handler(get_pass, content_types=types.ContentType.PHOTO, state=UserGet.get_pass)
    dp.register_message_handler(get_self, content_types=types.ContentType.PHOTO, state=UserGet.get_self)
    dp.register_message_handler(get_time, state=UserGet.get_time)
    dp.register_message_handler(get_card, state=UserGet.get_card)
    dp.register_callback_query_handler(get_model, BackFilter(), state=UserGet.get_model)
    dp.register_callback_query_handler(get_phone, BackFilter(), state=UserGet.get_phone)
    dp.register_callback_query_handler(get_color, BackFilter(), state=UserGet.get_color)
    dp.register_callback_query_handler(get_type, BackFilter(), state=UserGet.get_type)
    dp.register_callback_query_handler(get_conf, BackFilter(), state=UserGet.get_conf)
    dp.register_callback_query_handler(back, state="*")
