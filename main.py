from telethon import TelegramClient, events
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
your_user_id = int(os.getenv("USER_ID"))

channels = [
    'https://t.me/flats_for_friend',
    'https://t.me/nebabushkin_msk',
    'https://t.me/lvngrm_msk'
]
hashtags = ['#аренда1к', '#однушка', '#арендаевродвушка']

client = TelegramClient('flatbot_session', api_id, api_hash)

@client.on(events.NewMessage(chats=channels))
async def handler(event):
    message = event.message.message or ""
    if any(tag in message.lower() for tag in hashtags):
        post_link = f"https://t.me/{event.chat.username}/{event.id}"
        caption = "🏡 Объявление по фильтру:\n{}\n\n{}".format(post_link, message)"
        if event.message.media:
            await client.send_file(your_user_id, file=event.message.media, caption=caption)
        else:
            await client.send_message(your_user_id, caption)

async def main():
    await client.start()
    print("👀 Бот следит за квартирами...")
    await client.run_until_disconnected()

asyncio.run(main())
