import os
import asyncio
import aiohttp
from aiogram import Bot

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID"))

bot = Bot(token=TELEGRAM_BOT_TOKEN)

sent_upbit = set()
sent_binance = set()

async def fetch_upbit():
    url = "https://api-manager.upbit.com/api/v1/notices?language=ko"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()
                for item in data['data']['list']:
                    title = item['title']
                    notice_id = item['id']
                    link = f"https://upbit.com/service_center/notice/{notice_id}"
                    if ("上币" in title or "支持" in title or "交易" in title) and notice_id not in sent_upbit:
                        sent_upbit.add(notice_id)
                        text = f"🚀【Upbit 上币公告】\n\n📌{title}\n🔗{link}"
                        await bot.send_message(TELEGRAM_CHAT_ID, text)
    except Exception as e:
        print(f"Upbit fetch error: {e}")

async def fetch_binance():
    url = "https://www.binance.com/bapi/composite/v1/public/cms/article/list/query"
    params = {
        "catalogId": "48",
        "pageSize": 5,
        "pageNo": 1
    }
    headers = {"Content-Type": "application/json"}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, headers=headers) as resp:
                data = await resp.json()
                for article in data['data']['articles']:
                    title = article['title']
                    code = article['code']
                    link = f"https://www.binance.com/zh-CN/support/announcement/{code}"
                    if ("上线" in title or "新币种" in title) and code not in sent_binance:
                        sent_binance.add(code)
                        text = f"🚀【Binance 上币公告】\n\n📌{title}\n🔗{link}"
                        await bot.send_message(TELEGRAM_CHAT_ID, text)
    except Exception as e:
        print(f"Binance fetch error: {e}")

async def main():
    while True:
        await fetch_upbit()
        await fetch_binance()
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
