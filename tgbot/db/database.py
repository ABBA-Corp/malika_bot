from gino import Gino
from gino.schema import GinoSchemaVisitor

from tgbot.config import Config

db = Gino()


async def create_db(bot):
    config: Config = bot.get('config')
    await db.set_bind(f"postgresql://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.database}")
    db.gino: GinoSchemaVisitor
    await db.gino.create_all()
