from dataclasses import dataclass

from environs import Env


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_ids: list
    channel_ids: str
    use_redis: bool


@dataclass
class Miscellaneous:
    sentry_dsn: str
    api_user: str
    api_pass: str
    front_url: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            channel_ids=str("CHANNEL_IDS"),
            use_redis=env.bool("USE_REDIS")
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME')
        ),
        misc=Miscellaneous(
            sentry_dsn=env.str('SENTRY_DSN'),
            api_user=env.str('API_USER'),
            api_pass=env.str('API_PASS'),
            front_url=env.str('FRONT_URL')
        )
    )
