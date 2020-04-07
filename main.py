from core import bot, dp, is_registered
from aiogram import executor, types
from daftar import formulir_daftar, daftar, menu


@dp.message_handler(commands='help')
async def close_cmd_handler(message: types.Message):
    keyboard_markup = types.ReplyKeyboardRemove()
    await message.answer("1.\tStart Bot\t\t\t\t\t\t\t\t\t\t\t\t: /start\n"
                         "2.\tDaftar\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t: /daftar\n"
                         "3.\tMenu\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t: /menu\n"
                         "4.\tBantuan Ini\t\t\t\t\t\t\t: /help", reply_markup=keyboard_markup)


@dp.message_handler(commands='Close!')
async def close_cmd_handler(message: types.Message):
    keyboard_markup = types.ReplyKeyboardRemove()
    await message.answer("Terimasih, untuk membuka menu lagi silahkan ketik : /menu atau /help", reply_markup=keyboard_markup)


@dp.message_handler(commands='menu')
async def menu_cmd_handler(message: types.Message):
    await menu(message)


@dp.message_handler(commands='daftar')
async def register_cmd_handler(message: types.Message):
    await daftar(message)


@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message):
    # default row_width is 3, so here we can omit it actually
    # kept for clearness
    if not message.from_user.is_bot:
        registered: bool = await is_registered(message.from_user.id)
        if registered:
            await message.answer(f"selamat datang kembali "
                                 f"{message.from_user['first_name']} ☺️"
                                 f", perlu bantuan? lakukan perintah /help ")
            await menu(message)
        else:
            keyboard_markup = types.ReplyKeyboardRemove()
            await message.answer(f"Selamat Datang {message.from_user.first_name} ☺️",reply_markup=keyboard_markup)
            await daftar(message)
    else:
        await message.answer("bot tidak di perbolehkan menggunakan ini , perlu bantuan? lakukakan perintah /help")


# Use multiple registrators. Handler will execute when one of the filters is OK
@dp.callback_query_handler(text='tolak_daftar')  # if cb.data == 'no'
@dp.callback_query_handler(text='daftar')  # if cb.data == 'yes'
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
    answer_data = query.data
    await query.answer(f'You answered with {answer_data!r}')
    if answer_data == 'daftar':
        keyboard_markup = types.ReplyKeyboardRemove()
        await query.message.answer("untuk daftar balas pesan ini data dengan format seperti berikut", reply_markup=keyboard_markup)
        await query.message.answer("#DAFTAR\n"
                                   "\nKabupaten : kabupaten kamu"
                                   "\nKecamatan :  kecamatan kamu"
                                   "\nNama Outlet :  nama outlet kamu"
                                   "\nNomor MKios : nomor mkios kamu")
    elif answer_data == 'tolak_daftar':
        keyboard_markup = types.ReplyKeyboardRemove()
        await bot.send_message(query.from_user.id, text=":( " ,reply_markup=keyboard_markup)
        text = 'jika anda berubah fikiran silahkan daftar dengan perintah /daftar atau /help'
        await bot.send_message(query.from_user.id, text)
    else:
        text = f'Unexpected callback data {answer_data!r}!'
        await bot.send_message(query.from_user.id, text)


@dp.callback_query_handler(text='buy_sp_reg')  # if cb.data == 'no'
@dp.callback_query_handler(text='buy_sp_data')  # if cb.data == 'yes'
async def order_callback_handler(query: types.CallbackQuery):
    registered: bool = await is_registered(query.from_user.id)
    if not registered:
        await query.message.reply("Sorry, Kamu Belum Terdaftar 😝", reply_markup=types.ReplyKeyboardRemove())
    else:
        answer_data = query.data
        await query.answer(f'You answered with {answer_data!r}')
        if answer_data == 'buy_sp_reg':
            await query.message.answer(
                "Fitur Belanjunya belum jadi mas, wkwkw 🤣",
                reply_markup=types.ReplyKeyboardRemove()
            )
        elif answer_data == 'buy_sp_data':
            await query.message.answer(
                "Fitur Belanjunya belum jadi mas, wkwkw 🤣",
                reply_markup=types.ReplyKeyboardRemove()
            )
        else:
            text = f'Unexpected callback data {answer_data!r}!'
            await bot.send_message(query.from_user.id, text)


@dp.message_handler()
async def all_message_handler(message: types.Message):
    if '#DAFTAR\n' and 'Kabupaten' and 'Kecamatan' and 'Nama Outlet' and 'Nomor MKios' in message.text:
        registered: bool = await is_registered(message.from_user.id)
        if not registered:
            await formulir_daftar(message)
        else:
            await message.answer("Sebelumnya Anda Sudah Terdaftar, Perlu bantuan ? /help",
                                 reply_markup=types.ReplyKeyboardRemove())
    if message.text == "(_Belanja_)":
        registered: bool = await is_registered(message.from_user.id)
        if not registered:
            await message.reply("Kamu Belum Terdaftar 😝", reply_markup=types.ReplyKeyboardRemove())
        else:
            keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
            text_and_data = (
                ('SP Reg', 'buy_sp_reg'),
                ('SP Data', 'buy_sp_data'),
            )
            row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
            keyboard_markup.row(*row_btns)
            await message.reply("Silahkan Dipilih Productnya", reply_markup=keyboard_markup)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)