import asyncio
import logging
import sentry_sdk
import uvicorn

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.api.api_cmds import create_app
from tgbot.config import load_config
from tgbot.db.add_to_database import on_start_add_admin
from tgbot.db.database import create_db
from tgbot.db.db_cmds import get_admins
from tgbot.filters.admin import AdminFilter
from tgbot.filters.back import BackFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.echo import register_echo
from tgbot.handlers.user import register_user
from tgbot.middlewares.environment import EnvironmentMiddleware

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(BackFilter)


def register_all_handlers(dp):
    register_admin(dp)
    register_user(dp)
    # debug
    # register_echo(dp)


async def main():

    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    config = load_config(".env")

    sentry_sdk.init(
        dsn=config.misc.sentry_dsn,
        traces_sample_rate=1.0
    )

    logger.info("Starting bot")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config
    await create_db(bot)
    await on_start_add_admin(config)
    bot['admins'] = await get_admins()

    # create_app()
    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)


    # start

    try:
        await dp.skip_updates()
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == "__main__":
    try:
        app = asyncio.run(create_app())

        @app.on_event("startup")
        async def startup_event():
            asyncio.create_task(main())

        uvicorn.run(app, host="127.0.0.1", port=8090)
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
