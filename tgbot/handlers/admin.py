from aiogram import Dispatcher, types
from aiogram.types import Message, InputFile

from tgbot.db.db_cmds import add_admins
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


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
    dp.register_message_handler(add_admin, commands=["adminadd"], state="*", is_admin=True)
    dp.register_message_handler(get_doc, content_types=types.ContentType.DOCUMENT, state="*", is_admin=True)