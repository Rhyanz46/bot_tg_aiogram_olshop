from aiogram import types
from core import regex_special_character, is_registered
from database import cnx
from datetime import datetime


async def add_user(user: dict):
    cursor = cnx.cursor(buffered=True)
    query = ("INSERT INTO user "
             "(telegram_id, telegram_username, kabupaten, kecamatan, nama_outlet, nomor_mkios, tgl_registrasi) "
             "VALUES (%(telegram_id)s, '', %(kabupaten)s, %(kecamatan)s, %(nama_outlet)s, %(nomor_mkios)s, %(tgl_registrasi)s)")
    cursor.execute(query, user)
    print(user)
    cnx.commit()


async def menu(message: types.Message):
    registered: bool = await is_registered(message.from_user.id)
    if not registered:
        await message.answer("anda belum terdaftar, butuh bantuan ? lakukan perintah /help",
                             reply_markup=types.ReplyKeyboardRemove())
    else:
        keyboard_markup = types.ReplyKeyboardMarkup(row_width=2)
        text_and_data = (('(_Belanja_)'), ('/Close!'))
        row_btns = (types.KeyboardButton(text) for text in text_and_data)
        keyboard_markup.row(*row_btns)
        await message.answer("Pilih Menu : ", reply_markup=keyboard_markup)


async def formulir_daftar(message: types.Message):
    # data: str = ''.join(e for e in message.text if e.isalnum())
    data: list = message.text.split('\n')
    form_data: dict = {"telegram_id": message.from_user.id, "tgl_registrasi": datetime.now().date()}
    valid: bool = True
    for item in data:
        if 'Kabupaten' in item:
            kabupaten = item.replace('Kabupaten : ', '')
            if regex_special_character.search(kabupaten):
                karakter = kabupaten[regex_special_character.search(kabupaten).span()[0]]
                valid = False
                await message.answer(f"Kabupaten tidak boleh memiliki special karakter {karakter}")
            form_data["kabupaten"] = kabupaten.strip().lower()
        if 'Kecamatan' in item:
            kecamatan = item.replace('Kecamatan : ', '')
            form_data["kecamatan"] = kecamatan.strip().lower()
        if 'Nama Outlet' in item:
            nama_oulet = item.replace('Nama Outlet : ', '')
            form_data["nama_outlet"] = nama_oulet.strip()
        if 'Nomor MKios' in item:
            nomor_mkios = item.replace('Nomor MKios : ', '')
            try:
                nomor_mkios = int(nomor_mkios.strip())
            except:
                await message.answer("mkios harusnya berupa nomor")
                valid = False
            form_data["nomor_mkios"] = nomor_mkios
        if not valid:
            form_data = {}
    if not form_data:
        await message.answer(f"Pastikan data anda benar")
    else:
        await add_user(form_data)
        await message.answer(f"Terimakasih {message.from_user.first_name}, Anda sudah terdaftar :) ")
        await menu(message)


async def daftar(message: types.Message):
    registered = await is_registered(message.from_user.id)
    if registered:
        keyboard_markup = types.ReplyKeyboardRemove()
        await message.answer(f"maaf {message.from_user['first_name']}, anda sudah terdaftar, "
                             f"butuh bantuan ? lakukan perintah /help ",
                             reply_markup=keyboard_markup)
    else:
        keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
        text_and_data = (
            ('Daftar!', 'daftar'),
            ('No!', 'tolak_daftar'),
        )
        row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
        keyboard_markup.row(*row_btns)
        keyboard_markup.add(
            # url buttons have no callback data
            types.InlineKeyboardButton('Baca Aturan', url='https://twitter.com'),
        )
        await message.reply("Silahkan Daftarkan Diri Anda", reply_markup=keyboard_markup)