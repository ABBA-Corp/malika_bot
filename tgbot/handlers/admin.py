from aiogram import Dispatcher, types
from aiogram.types import Message, CallbackQuery, InputFile

from tgbot.db.db_cmds import add_admins, update_order
from tgbot.misc.get_info import add_or_update_db


async def admin_start(m: Message):
    await m.reply("Salom, admin! 👋. Excelni manabu korinishda yuboring")
    await m.bot.send_document(m.from_user.id, document=InputFile("example.xlsx"))


async def get_doc(m: Message):
    doc = str(m.from_user.id)
    await m.document.download(destination_file=f"{doc}.xlsx")
    await m.answer("⏳")
    await m.answer("Iltimos biroz kutib turing")
    await add_or_update_db(doc, m)


async def add_admin(m: Message):
    admin_id = m.get_args()
    if not admin_id:
        return await m.answer("Admin qo'shmohchi bo'lsangiz manabu formatda qo'shing:\n /adminadd 111111111")
    if await add_admins(admin_id=int(admin_id), m=m):
        ls = m.bot.get("admins")
        ls.append(int(admin_id))
        m.bot["admins"] = ls


async def get_conf(c: CallbackQuery):
    if c.data.startswith('co'):
        order_id = str(c.data).replace("co", "")
        await update_order(id=int(order_id), status=True)
        await c.message.edit_text(f"🆔 So'rov id: {order_id}\n"
                                  f"✅ Qabul qilindi")
    else:
        order_id = str(c.data).replace("ca", "")
        await c.message.edit_text(f"🆔 So'rov id: {order_id}\n"
                                  f"❌ Bekor qilindi")
    config = c.bot.get("config")
    await c.message.answer(config.misc.front_url+str(order_id))


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, chat_type=types.ChatType.PRIVATE, commands=["start"], state="*", is_admin=True)
    dp.register_message_handler(add_admin, chat_type=types.ChatType.PRIVATE, commands=["adminadd"], state="*", is_admin=True)
    dp.register_message_handler(get_doc, chat_type=types.ChatType.PRIVATE, content_types=types.ContentType.DOCUMENT, state="*", is_admin=True)
    dp.register_callback_query_handler(get_conf, chat_type=[types.ChatType.GROUP, types.ChatType.CHANNEL], state='*')
