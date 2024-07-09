from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.private & filters.text)
async def handle_message(client, message: Message):
    # Proses pesan yang diterima dari bot kedua
    pesan = message.text
    link = "https://example.com"  # Ganti dengan link yang sesuai
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Tap URL", url=f'https://telegram.me/share/url?url={link}')]])

    # Kirim pesan ke channel menggunakan bot pertama
    await client.send_message(
        chat_id=CHANNEL_ID,
        text=pesan,
        reply_markup=reply_markup
    )