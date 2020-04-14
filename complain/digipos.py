from aiogram import types


async def digipos_complain_confirmation_handler(dp, state_obj):
    user_form = state_obj['state']
    reset_proxy = state_obj['methods']['reset']
    default_proxy = state_obj['methods']['default']

    @dp.callback_query_handler(text='ya_digipos_complain')  # if cb.data == 'no'
    @dp.callback_query_handler(text='batal_digipos_complain')  # if cb.data == 'yes'
    async def handler(query: types.CallbackQuery, state: user_form):
        answer_data = query.data
        async with state.proxy() as proxy:
            if not proxy.get('complain_detail'):
                return await query.message.answer(
                    "Gagal, Ulangi Proses Komplain",
                    reply_markup=types.ReplyKeyboardRemove()
                )
            print(answer_data)
            print(proxy)


async def digipos_complain_handler(message: types.Message, state, reset_proxy, default_proxy):
    from core import is_registered, User
    registered: User = await is_registered(message.from_user.id)
    if not registered.ok:
        await message.reply("Sorry, Kamu Belum Terdaftar 😝", reply_markup=types.ReplyKeyboardRemove())
    async with state.proxy() as proxy:
        await default_proxy(proxy, addtions={
            'complain_detail': None,
            'complain_pay_method': None,
            'complain_versi_apk_dipos': None,
            'complain_channel_lain': None
        })
        if not proxy.get('complain_detail'):
            proxy['complain_detail'] = message.text
            return await message.answer(
                "Methode Pembayarannya apa ? ",
                reply_markup=types.ReplyKeyboardRemove()
            )
        if not proxy.get('complain_pay_method'):
            proxy['complain_pay_method'] = message.text
            return await message.answer(
                "VERSI APK digiposnya ? ",
                reply_markup=types.ReplyKeyboardRemove()
            )
        if not proxy.get('complain_versi_apk_dipos'):
            proxy['complain_versi_apk_dipos'] = message.text
            return await message.answer(
                "ADA Channel Lain ? ",
                reply_markup=types.ReplyKeyboardRemove()
            )
        if not proxy.get('complain_channel_lain'):
            proxy['complain_channel_lain'] = message.text
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
