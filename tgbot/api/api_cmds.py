import os
import secrets
import aiofiles

from typing import List

from aiogram import Bot

from fastapi import Depends, FastAPI, HTTPException, status, File, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware

from tgbot.api.send_group import group
from tgbot.config import load_config
from tgbot.db.db_cmds import add_order, get_order, get_models, get_phones, get_list_phones

config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')


async def create_app() -> FastAPI:
    app = FastAPI()
    security = HTTPBasic()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

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

    @app.get("/api/v1/confirm")
    async def user_confirm(order_id: int):
        await bot.send_message(chat_id=config.tg_bot.channel_ids, text=f"🆔 Sorov id: {order_id}\n"
                                                                       "✅ Foudalanuvchi tominidan qabul qilindi!")
        return {"Status": "accept"}

    @app.post("/api/v1/order/create")
    async def create_order(id: int = Form(...),
                           name: str = Form(...),
                           number: str = Form(...),
                           card: str = Form(...),
                           time: str = Form(...),
                           model: str = Form(...),
                           phone: str = Form(...),
                           color: str = Form(...),
                           passport: str = Form(...),
                           selfie: str = Form(...),
                           type: str = Form(...),
                           ):
        # if len(files) == 2:
        #     path = os.getcwd()
        #     names = []
        #     for file in files:
        #         destination_file_path = f"{path}/tgbot/media/{file.filename}"
        #         names.append(destination_file_path)
        #         async with aiofiles.open(destination_file_path, 'wb') as out_file:
        #             while content := await file.read(1024):
        #                 await out_file.write(content)
        # order = await add_order(name=name, number=number, passport=names[0],
        #                         selfie=names[1], card=card, time=time,
        #                         model=model, phone=phone, color=color,
        #                         type=type, status=False)

        await group(bot, config, id=id, name=name, number=number, card=card, time=time, model=model, phone=phone,
                    color=color, passport=passport, selfie=selfie, type=type)
        return {"status": "Created"}

    @app.post("/api/v1/order/file/{pk}")
    async def get_file(pk: int, username: str = Depends(get_current_username)):
        order = await get_order(id=pk)
        print(order)
        if order is not None and order.file is not None:
            doc_type = order.file
            if doc_type[-3:] == "pdf":
                file_type = ".pdf"
            else:
                file_type = ".docx"
            return FileResponse(order.file, media_type="application/octet-stream", filename=f"{order.id}{file_type}")
        else:
            raise HTTPException(status_code=404, detail="order does not exist")

    @app.post("/api/v1/order/status/{pk}")
    async def check_order(pk: int, username: str = Depends(get_current_username)):
        order = await get_order(id=pk)
        if order is not None:
            return {"id": order.id,
                    "name": order.name,
                    "number": order.number,
                    "card": order.card,
                    "time": order.time,
                    "model": order.model,
                    "phone": order.phone,
                    "color": order.color,
                    "type": order.type,
                    "status": order.status}
        else:
            raise HTTPException(status_code=404, detail="order does not exist")

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

