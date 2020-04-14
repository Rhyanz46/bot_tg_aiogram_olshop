from aiogram import types


async def send_complain_or_not(message: types.Message, state):
    async with state.proxy() as proxy:
        print(proxy)
        keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
        text_and_data = (
            ('Kirim', 'ya_digipos_complain'),
            ('BATAL', 'batal_digipos_complain'),
        )
        row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
        keyboard_markup.row(*row_btns)
        return await message.answer(
            "Anda yakin dengan komplain anda ? ",
            reply_markup=keyboard_markup
        )


async def digipos_complain_confirmation_handler(dp, state_obj):
    user_form = state_obj['state']
    reset_proxy = state_obj['methods']['reset']
    default_proxy = state_obj['methods']['default']

    @dp.callback_query_handler(text='req_photo_digipos_complain')  # if cb.data == 'no'
    @dp.callback_query_handler(text='no_req_photo_digipos_complain')  # if cb.data == 'no'
    @dp.callback_query_handler(text='ya_digipos_complain')  # if cb.data == 'no'
    @dp.callback_query_handler(text='batal_digipos_complain')  # if cb.data == 'yes'
    async def handler(query: types.CallbackQuery, state: user_form):
        answer_data = query.data
        async with state.proxy() as proxy:
            if not proxy.get('complain_digipos_detail'):
                return await query.message.answer(
                    "Gagal, Ulangi Proses Komplain",
                    reply_markup=types.ReplyKeyboardRemove()
                )
            if answer_data == 'req_photo_digipos_complain':
                proxy['complain_digipos_photo_require'] = True
                return await query.message.answer(
                    "Silahkan upload gambar kesini.",
                    reply_markup=types.ReplyKeyboardRemove()
                )
            if answer_data == 'no_req_photo_digipos_complain':
                await query.message.answer(
                    "Tidak perlu khawatir jika anda tidak memiliki bukti, kami akan berusaha meninjaunya",
                    reply_markup=types.ReplyKeyboardRemove()
                )
                await send_complain_or_not(query.message, state)
            if answer_data == 'batal_digipos_complain':
                await reset_proxy(proxy)
                return await query.message.answer(
                    "Anda telah membatalkan proses complain",
                    reply_markup=types.ReplyKeyboardRemove()
                )
            print(answer_data)


async def digipos_complain_handler(message: types.Message, state, reset_proxy, default_proxy):
    from core import is_registered, User
    registered: User = await is_registered(message.from_user.id)
    if not registered.ok:
        await message.reply("Sorry, Kamu Belum Terdaftar 😝", reply_markup=types.ReplyKeyboardRemove())
    async with state.proxy() as proxy:
        await default_proxy(proxy, addtions={
            'complain_digipos_detail': None,
            'complain_digipos_pay_method': None,
            'complain_digipos_versi_apk_dipos': None,
            'complain_digipos_channel_lain': None,
            'complain_digipos_photo_require': False,
            'complain_digipos_photo': None
        })
        if not proxy.get('complain_digipos_detail'):
            proxy['complain_digipos_detail'] = message.text
            return await message.answer(
                "Methode Pembayarannya apa ? ",
                reply_markup=types.ReplyKeyboardRemove()
            )
        if not proxy.get('complain_digipos_pay_method'):
            proxy['complain_digipos_pay_method'] = message.text
            return await message.answer(
                "VERSI APK digiposnya ? ",
                reply_markup=types.ReplyKeyboardRemove()
            )
        if not proxy.get('complain_digipos_versi_apk_dipos'):
            proxy['complain_digipos_versi_apk_dipos'] = message.text
            return await message.answer(
                "ADA Channel Lain ? ",
                reply_markup=types.ReplyKeyboardRemove()
            )
        # req_photo_digipos_complain
        if not proxy.get('complain_digipos_channel_lain'):
            proxy['complain_digipos_channel_lain'] = message.text
            keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
            text_and_data = (
                ('Upload Foto Bukti', 'req_photo_digipos_complain'),
                ('Tidak', 'no_req_photo_digipos_complain'),
            )
            row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
            keyboard_markup.row(*row_btns)
            return await message.answer(
                "Ada bukti berupa gambar ? jika ada, apakah anda mau melampirkannya ? \n"
                "ini akan membuat proses peninjuan lebih gampang.",
                reply_markup=keyboard_markup
            )
