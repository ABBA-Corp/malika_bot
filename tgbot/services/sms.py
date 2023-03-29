import aiohttp


async def send_url(number, url):
    sms_data = {"messages": [{"recipient": f"{number}",
                              "message-id": "abc000000003",
                              "sms": {
                                  "originator": "3700",
                                  "content": {
                                      "text": f"Markab bot so'rovingiz qabul qilindi: {url}"}}}]}
    async with aiohttp.ClientSession() as session:
        async with session.post(url="http://91.204.239.44/broker-api/send",
                                auth=aiohttp.BasicAuth('markab', 'i^R_h8A#g95E'),
                                json=sms_data) as resposne:
            pass