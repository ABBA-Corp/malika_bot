import aiohttp

from ..config import load_config


async def update_order(**kwargs):
    if kwargs["file"] is None:
        data = {"status": kwargs["status"]}
    else:
        data = {"file": open(kwargs["file"], "rb")}
    async with aiohttp.ClientSession() as session:
        async with session.patch(url=f"{load_config().misc.api_url}order/update/{kwargs['order_id']}", data=data) as response:
            return await response.json()


async def add_order(**kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f"{load_config().misc.api_url}order/create/bot",
                                data={"name": kwargs["name"],
                                      "number": kwargs["number"],
                                      "passport": open(kwargs["passport"], "rb"),
                                      "selfie": open(kwargs["selfie"], "rb"),
                                      "card": kwargs["card"],
                                      "time": kwargs["time"],
                                      "model": kwargs["model"],
                                      "phone": kwargs["phone"],
                                      "color": kwargs["color"],
                                      "type": kwargs["type"],
                                      "isbot": "ye"}) as response:
            res = await response.json()
            return res["id"]


async def get_models(name=None):
    if name is None:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"{load_config().misc.api_url}model/list") as response:
                return await response.json()


async def get_order(order_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{load_config().misc.api_url}order/status/{order_id}") as response:
            return await response.json()


async def get_phones(model='default', name='default'):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{load_config().misc.api_url}phones/filter", params={"model": model,
                                                                                         "name": name}) as response:
            return await response.json()
