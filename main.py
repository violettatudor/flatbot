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
    if not event.message:
        return  # Пропускаем системные или странные сообщения

    message = event.message.message
    if not message:
        return  # Пропускаем сообщения без текста

    message = message.strip()
    if not message:
        return

    if any(tag in message.lower() for tag in hashtags):
        if not event.chat or not event.chat.username:
            return  # Без username не собрать ссылку

        post_link = f"https://t.me/{event.chat.username}/{event.id}"
        caption = "🏡 Объявление по фильтру:\n{}\n\n{}".format(post_link, message)

        try:
            if event.message.media:
                await client.send_file(your_user_id, file=event.message.media, caption=caption)
            else:
                await client.send_message(your_user_id, caption)
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")

async def main():
    await client.start()
    print("👀 Бот следит за квартирами...")
    await client.run_until_disconnected()

asyncio.run(main())
