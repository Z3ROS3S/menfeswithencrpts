from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import asyncio

# Inisialisasi variabel untuk menyimpan data pengguna
user_data = {}

@Client.on_message(filters.command('start') & filters.private)
async def start(client, message: Message):
    user_id = message.from_user.id
    user_data[user_id] = {}
    await message.reply(
        "Hallo Pilihlah Jenis Kelamin Anda",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Cowo", callback_data="gender_cowo"), InlineKeyboardButton("Cewe", callback_data="gender_cewe")]
        ])
    )

@Client.on_callback_query(filters.regex(r"^gender_"))
async def gender_callback(client, query: CallbackQuery):
    user_id = query.from_user.id
    gender = query.data.split("_")[1]
    user_data[user_id]['gender'] = gender
    await query.message.edit_text("Content Donate\nSex    No", reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("Sex", callback_data="content_sex"), InlineKeyboardButton("No", callback_data="content_no")]
    ]))

@Client.on_callback_query(filters.regex(r"^content_"))
async def content_callback(client, query: CallbackQuery):
    user_id = query.from_user.id
    content = query.data.split("_")[1]
    user_data[user_id]['content'] = content
    await query.message.edit_text("✏️: Masukan Pesan Kamu")

@Client.on_message(filters.private & ~filters.command)
async def handle_message(client, message: Message):
    user_id = message.from_user.id
    if 'content' in user_data.get(user_id, {}):
        user_data[user_id]['message'] = message.text
        await message.reply("Sent Your Media For Share")
    elif 'message' in user_data.get(user_id, {}):
        if message.photo or message.video:
            user_data[user_id]['media'] = message.photo or message.video
            await message.reply("Porsses Loading...")
            await asyncio.sleep(2)  # Simulasi loading
            await message.reply("Porses Selesai! Terimakasih Sudah Donasi!")
            await send_to_channel(client, user_id)
        else:
            await message.reply("Silakan kirim foto atau video.")

async def send_to_channel(client, user_id):
    data = user_data[user_id]
    gender = data['gender']
    content = data['content']
    pesan = data['message']
    media = data['media']
    link = "https://example.com"  # Ganti dengan link yang sesuai
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Tap URL", url=f'https://telegram.me/share/url?url={link}')]])

    # Kirim pesan ke channel menggunakan bot kedua
    sent_message = await client.send_message(
        chat_id=CHANNEL_ID_2,
        text=f"Hello Member Disinih Donasi Nih\nGender : {gender}\nContent : {content}",
        reply_markup=reply_markup
    )

    # Kirim pesan ke bot pertama untuk membalas pesan di channel
    await client.send_message(
        chat_id=CHANNEL_ID,
        text=f"Halo Dek\n\n🔁 Tap URL",
        reply_to_message_id=sent_message.message_id,
        reply_markup=reply_markup
    )

    del user_data[user_id] 