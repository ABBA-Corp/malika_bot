import openpyxl
from aiogram.types import Message

from tgbot.db.db_cmds import add_or_update


async def add_or_update_db(doc, m: Message):
    book = openpyxl.load_workbook(doc + '.xlsx', read_only=True)
    sheet = book.active
    if sheet['A1'].value is None:
        return await m.answer('Xato formatda yuborildi. Iltimos qayta tekshirib yuboring. ❌')
    row_count = len([row for row in sheet if not all([cell.value is None for cell in row])])
    for i in range(2, row_count+1):
        if sheet[f'A{i}'].value is not None:
            await add_or_update(name=str(sheet[f'A{i}'].value), model=str(sheet[f'B{i}'].value),
                                color=str(sheet[f'C{i}'].value), month_3=str(sheet[f'D{i}'].value),
                                month_4=str(sheet[f'E{i}'].value),
                                month_6=str(sheet[f'F{i}'].value), month_8=str(sheet[f'G{i}'].value),
                                month_12=str(sheet[f'H{i}'].value), minimum=str(sheet[f'I{i}'].value))
        else:
            return await m.answer(f'Faylda A{i} bo\'sh')
    await m.answer('✅')
    return await m.answer('Import muvaffaqiyatli yakunlandi ✅')