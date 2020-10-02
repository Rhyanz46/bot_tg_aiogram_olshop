from aiogram import types
from core import regex_special_character, is_registered, User
from database import DBConnection


async def add_user(user: dict):
    cnx = DBConnection.get_connection().connection()
    cursor = cnx.cursor(buffered=True)
    query = ("INSERT INTO user "
             "(telegram_id, telegram_username, kabupaten, kecamatan, nama_outlet, nomor_mkios) "
             "VALUES (%(telegram_id)s, '', %(kabupaten)s, %(kecamatan)s, %(nama_outlet)s, %(nomor_mkios)s)")
    cursor.execute(query, user)
    cnx.commit()


async def menu(message: types.Message):
    if message.chat.type == 'group':
        return await message.answer(f"Perintah ini tidak berlaku disini, jika anda perlu bantuan saya, "
                                    f"Private Message ☺️")
    registered: User = await is_registered(message.from_user.id)
    if not registered.ok:
        await message.answer("anda belum terdaftar, butuh bantuan ? lakukan perintah /help",
                             reply_markup=types.ReplyKeyboardRemove())
    else:
        keyboard_markup = types.ReplyKeyboardMarkup(row_width=2)
        # text_and_data = (('(_Belanja_)'), ('(_Komplain_)'))
        text_and_data = (('(_Komplain_)'),)
        row_btns = (types.KeyboardButton(text) for text in text_and_data)
        keyboard_markup.row(*row_btns)
        text_and_data = (('/Close!'),)
        row_btns = (types.KeyboardButton(text) for text in text_and_data)
        keyboard_markup.row(*row_btns)
        await message.answer("Pilih Menu : ", reply_markup=keyboard_markup)


async def formulir_daftar(message: types.Message):
    registered: User = await is_registered(message.from_user.id)
    if not registered.ok:
        data: list = message.text.split('\n')
        form_data: dict = {"telegram_id": message.from_user.id}
        for item in data:
            if 'Kabupaten' in item:
                kabupaten = item.split('Kabupaten : ')
                if len(kabupaten) == 1:
                    return await message.answer(f"Masukkan format Kabupaten dengan benar")
                kabupaten = kabupaten[1]
                if regex_special_character.search(kabupaten):
                    karakter = kabupaten[regex_special_character.search(kabupaten).span()[0]]
                    return await message.answer(f"Kabupaten tidak boleh memiliki special karakter {karakter}")
                if len(kabupaten.strip()) > 149:
                    return await message.answer(f"Kabupaten tidak boleh lebih dari 149 karakter")
                form_data["kabupaten"] = kabupaten.strip().lower()
            if 'Kecamatan' in item:
                kecamatan = item.split('Kecamatan : ')
                if len(kecamatan) == 1:
                    return await message.answer(f"Masukkan format Kecamatan dengan benar")
                kecamatan = kecamatan[1]
                if len(kecamatan.strip()) > 149:
                    return await message.answer(f"Kecamatan tidak boleh lebih dari 149 karakter")
                form_data["kecamatan"] = kecamatan.strip().lower()
            if 'Nama Outlet' in item:
                nama_oulet = item.split('Nama Outlet : ')
                if len(nama_oulet) == 1:
                    return await message.answer(f"Masukkan format Nama Outlet dengan benar")
                nama_oulet = nama_oulet[1]
                if len(nama_oulet.strip()) > 149:
                    return await message.answer(f"Nama Outlet tidak boleh lebih dari 149 karakter")
                form_data["nama_outlet"] = nama_oulet.strip()
            if 'Nomor MKios' in item:
                nomor_mkios = item.split('Nomor MKios : ')
                if len(nomor_mkios) == 1:
                    return await message.answer(f"Masukkan format Nomor MKios dengan benar")
                nomor_mkios = nomor_mkios[1]
                if len(nomor_mkios.strip()) > 29:
                    return await message.answer(f"Nomor MKios tidak boleh lebih dari 29 karakter")
                try:
                    nomor_mkios = int(nomor_mkios.strip())
                except:
                    return await message.answer("mkios harusnya berupa nomor")
                form_data["nomor_mkios"] = nomor_mkios
        await add_user(form_data)
        await message.answer(f"Terimakasih {message.from_user.first_name}, Pendaftaran Anda Berhasil :) ")
        await menu(message)
    else:
        return await message.answer("Sebelumnya Anda Sudah Terdaftar, Perlu bantuan ? /help",
                                    reply_markup=types.ReplyKeyboardRemove())


async def daftar(message: types.Message):
    registered: User = await is_registered(message.from_user.id)
    if registered.ok:
        keyboard_markup = types.ReplyKeyboardRemove()
        await message.answer(f"maaf {message.from_user['first_name']}, anda sudah terdaftar, "
                             f"butuh bantuan ? lakukan perintah /help ",
                             reply_markup=keyboard_markup)
    else:
        keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
        text_and_data = (
            ('Daftar!', 'daftar'),
        )
        row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
        keyboard_markup.row(*row_btns)
        await message.answer("Untuk pelayanan maksimal, tolong daftar dulu ya.. Klik Daftar dibawah ini", reply_markup=keyboard_markup)