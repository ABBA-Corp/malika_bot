from tgbot.db.db_cmds import add_admins


async def on_start_add_admin(config):
    for i in config.tg_bot.admin_ids:
        await add_admins(admin_id=i, typ=False)
