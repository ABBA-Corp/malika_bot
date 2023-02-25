import secrets

from aiogram import Bot, types
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from tgbot.api.schemas import Order
from tgbot.config import load_config
from tgbot.db.db_cmds import add_order, get_order, get_models, get_phones, get_list_phones
from tgbot.keyboards.inline import admin_conf_btn

config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')


async def create_app() -> FastAPI:
    app = FastAPI()
    security = HTTPBasic()

    async def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
        current_username_bytes = credentials.username.encode("utf8")
        correct_username_bytes = config.misc.api_user.encode("utf8")
        is_correct_username = secrets.compare_digest(
            current_username_bytes, correct_username_bytes
        )
        current_password_bytes = credentials.password.encode("utf8")
        correct_password_bytes = config.misc.api_pass.encode("utf8")
        is_correct_password = secrets.compare_digest(
            current_password_bytes, correct_password_bytes
        )
        if not (is_correct_username and is_correct_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Basic"},
            )
        return credentials.username

    @app.post("/api/v1/order/create")
    async def create_order(order: Order, username: str = Depends(get_current_username)):
        order_id = await add_order(name=order.name, number=order.number, passport=order.passport,
                                   selfie=order.selfie, card=order.card, time=order.time,
                                   model=order.model, phone=order.phone, color=order.color,
                                   type=order.type, status=False)
        media = types.MediaGroup()
        media.attach_photo(order.passport)
        media.attach_photo(order.selfie, caption=f"🆔 So'rov id: {order_id}\n"
                                                 f"👨 Ismi: {order.name}\n"
                                                 f"📞 Telefon raqami: {order.number}\n"
                                                 f"💳 Karta raqami: {order.card}\n"
                                                 f"💳 Karta muddati: {order.time}\n"
                                                 f"📱 Model: {order.phone}\n"
                                                 f"🎨 Rangi: {order.color}\n"
                                                 f"📆 Muddati: {order.type} oy\n")
        for i in config.tg_bot.channel_ids:
            await bot.send_media_group(chat_id=i, media=media)
            await bot.send_message(chat_id=i, text="Tasdiqlaysizmi? 👆", reply_markup=await admin_conf_btn(order_id))
        return {"status": "Created"}

    @app.post("/api/v1/order/status/{pk}")
    async def check_order(pk: int, username: str = Depends(get_current_username)):
        order = await get_order(id=pk)
        return {"id": order.id,
                "name": order.name,
                "number": order.number,
                "passport": order.passport,
                "selfie": order.selfie,
                "card": order.card,
                "time": order.time,
                "model": order.model,
                "phone": order.phone,
                "color": order.color,
                "type": order.type,
                "status": order.status}

    @app.post("/api/v1/models/list")
    async def list_models(username: str = Depends(get_current_username)):
        models = await get_models()
        res = {"models": []}
        for i in models:
            res["models"].append(i.model)
        return res

    @app.post("/api/v1/phones/filter")
    async def filter_phones(model: str, username: str = Depends(get_current_username)):
        models = await get_phones(model)
        res = {"phones": []}
        for i in models:
            res["phones"].append({"id": i.id,
                                  "model": i.model,
                                  "name": i.name,
                                  "color": i.color,
                                  "month_3": i.month_3,
                                  "month_4": i.month_4,
                                  "month_6": i.month_6,
                                  "month_8": i.month_8,
                                  "month_12": i.month_12,
                                  "minimum": i.minimum,
                                  "date": i.date})
        return res

    @app.post("/api/v1/phones/list")
    async def list_phones(username: str = Depends(get_current_username)):
        models = await get_list_phones()
        res = {"phones": []}
        for i in models:
            res["phones"].append({"id": i.id,
                                  "model": i.model,
                                  "name": i.name,
                                  "color": i.color,
                                  "month_3": i.month_3,
                                  "month_4": i.month_4,
                                  "month_6": i.month_6,
                                  "month_8": i.month_8,
                                  "month_12": i.month_12,
                                  "minimum": i.minimum,
                                  "date": i.date})
        return res
    return app
