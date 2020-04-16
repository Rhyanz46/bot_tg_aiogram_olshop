from aiogram import types


class DigiPosMenu:
    def __init__(self):
        self.value = None
        self.is_return = False
        self.something_to_return = None


def choose_menu_not_text(selected: str, msg: types.Message, state) -> DigiPosMenu:
    digipos_menu = DigiPosMenu()
    if type(msg.text) == str:
        async def output():
            return await msg.answer(
                "Pilih Menu, jangan masukkan text!",
                reply_markup=types.ReplyKeyboardRemove()
            )
        digipos_menu.is_return = True
        digipos_menu.something_to_return = output
    return digipos_menu


def keren(selected: str, msg: types.Message, state) -> DigiPosMenu:
    digipos_menu = DigiPosMenu()
    digipos_menu.value = msg.text
    return digipos_menu


async def upload_bukti_ask(message, position=None, state=None, reset_proxy=None, default_proxy=None):
    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    text_and_data = (
        ('Upload Foto Bukti', 'req_photo_digipos_complain'),
        ('Tidak', 'no_req_photo_digipos_complain'),
    )
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
    keyboard_markup.row(*row_btns)

    return await message.answer(
        "Jika km mempunyai bukti, silahkan di upload,",
        reply_markup=keyboard_markup
    )


async def send_complain_or_not(message: types.Message, proxy):
    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    text_and_data = (
        ('Tambah Foto Bukti', 'req_photo_digipos_complain'),
    )
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
    keyboard_markup.row(*row_btns)
    text_and_data = (
        ('Kirim Komplain', 'ya_digipos_complain'),
        ('BATAL', 'batal_digipos_complain'),
    )
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
    keyboard_markup.row(*row_btns)
    return await message.answer(
        "Anda yakin dengan komplain anda ? ",
        reply_markup=keyboard_markup
    )


async def response_upload_bukti(message, proxy):
    if not message.photo:
        # from core import reset_proxy
        # await reset_proxy(proxy)
        return await message.answer(
            "Upload Foto, bukan text",
            reply_markup=types.ReplyKeyboardRemove()
        )
    if not proxy['complain_digipos_photo']:
        proxy['complain_digipos_photo'] = [message.photo[-1].file_id]
    else:
        proxy['complain_digipos_photo'].append(message.photo[-1].file_id)
    await message.answer(
        "Dengan bukti yang anda kirim "
        "ini akan membuat proses peninjauan menjadi lebih mudah.",
        reply_markup=types.ReplyKeyboardRemove()
    )
    # sleep(2)
    proxy['complain_digipos_photo_require'] = False
    await send_complain_or_not(message, proxy)


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
                await send_complain_or_not(query.message, proxy)
            if answer_data == 'batal_digipos_complain':
                await reset_proxy(proxy)
                return await query.message.answer(
                    "Anda telah membatalkan proses complain",
                    reply_markup=types.ReplyKeyboardRemove()
                )
            if answer_data == 'ya_digipos_complain':
                from core import complain
                complain.complain = {
                    'type': 'digipos',
                    'kabupaten': proxy['complain_digipos_kabupaten'],
                    'kecamatan': proxy['complain_digipos_kecamatan'],
                    'id_outlet': proxy['complain_digipos_id_outlet'],
                    'nama_outlet': proxy['complain_digipos_nama_outlet'],
                    'no_mkios': proxy['complain_digipos_no_mkios'],
                    'no_pelanggan': proxy['complain_digipos_no_pelanggan'],
                    'tgl_transaksi': proxy['complain_digipos_tgl_transaksi'],
                    'detail': proxy['complain_digipos_detail'],
                    'pay_method': proxy['complain_digipos_pay_method'],
                    'versi_apk_dipos': proxy['complain_digipos_versi_apk_dipos'],
                    'channel_lain': proxy['complain_digipos_channel_lain'],
                    'photo': proxy['complain_digipos_photo']
                }
                await complain.send(query, state)


async def digipos_complain_handler(message: types.Message, state, reset_proxy, default_proxy):
    from core import is_registered, User
    registered: User = await is_registered(
        message.from_user.id
    )
    if not registered.ok:
        await message.reply(
            "Sorry, Kamu Belum Terdaftar 😝",
            reply_markup=types.ReplyKeyboardRemove()
        )
    async with state.proxy() as proxy:
        await default_proxy(proxy, addtions={
            'complain_digipos_kabupaten': None,
            'complain_digipos_kecamatan': None,
            'complain_digipos_id_outlet': None,
            'complain_digipos_nama_outlet': None,
            'complain_digipos_no_mkios': None,
            'complain_digipos_no_pelanggan': None,
            'complain_digipos_tgl_transaksi': None,
            'complain_digipos_detail': None,
            'complain_digipos_pay_method': None,
            'complain_digipos_versi_apk_dipos': None,
            'complain_digipos_channel_lain': None,
            'complain_digipos_photo_require': False,
            'complain_digipos_photo': None,
            'complain_digipos_progress': None
        })

        data_to_get = {
            0: {
                'menu': 'complain_digipos_detail'
            },
            1: {
                'menu': 'complain_digipos_kabupaten',
                'pesan': 'Masukkan Kabupaten Anda'
            },
            2: {
                'menu': 'complain_digipos_kecamatan',
                'pesan': 'Masukkan Kecamatan Anda'
            },
            3: {
                'menu': 'complain_digipos_id_outlet',
                'pesan': 'ID Outlet Anda'
            },
            4: {
                'menu': 'complain_digipos_nama_outlet',
                'pesan': 'Nama Outlet'
            },
            5: {
                'menu': 'complain_digipos_no_mkios',
                'pesan': 'No MKios',
                'response': keren,
            },
            6: {
                'menu': 'complain_digipos_no_pelanggan',
                'pesan': 'No HP yang bisa di hubungi'
            },
            7: {
                'menu': 'complain_digipos_tgl_transaksi',
                'pesan': 'Tanggal Transaksi'
            },
            8: {
                'menu': 'complain_digipos_pay_method',
                'pesan': 'Apa methode pembayaran yang anda gunakan ?'
            },
            9: {
                'menu': 'complain_digipos_versi_apk_dipos',
                'pesan': 'Masukkan VERSI APK DigiPos'
            },
            10: {
                'menu': 'complain_digipos_channel_lain',
                'pesan': 'Channel Lain (UMB)'
            },
            11: {
                'menu': 'complain_digipos_photo',
                'pesan': upload_bukti_ask,
                'response': choose_menu_not_text
            }
        }

        # pencegahan
        if proxy['complain_digipos_photo_require']:
            return await response_upload_bukti(message, proxy)
        # pencegahan

        try:
            if len(data_to_get) >= proxy['complain_digipos_progress']+1:
                proxy['complain_digipos_progress'] += 1
        except:
            proxy['complain_digipos_progress'] = 1

        try:
            pesan = data_to_get[proxy['complain_digipos_progress']]['pesan']
        except:
            pesan = data_to_get[proxy['complain_digipos_progress']-1]['pesan']
        if callable(pesan):
            await pesan(
                message,
                proxy['complain_digipos_progress'] + 1,
                state,
                reset_proxy,
                default_proxy
            )

        response = data_to_get[proxy['complain_digipos_progress'] - 1].get('response')
        if response:
            object_return: DigiPosMenu = response(
                proxy['complain_digipos_progress'] - 1,
                message, state
            )
            if not object_return.is_return:
                proxy[data_to_get[proxy['complain_digipos_progress'] - 1]['menu']] = object_return.value
            else:
                return await object_return.something_to_return()
        else:
            proxy[data_to_get[proxy['complain_digipos_progress'] - 1]['menu']] = message.text

        # complain_digipos_detail ditanya di file __init__
        if len(data_to_get) < proxy['complain_digipos_progress'] + 1:
            print(proxy)
            proxy['complain_digipos_progress'] -= 1

        if callable(pesan):
            return None
        return await message.answer(
            pesan,
            reply_markup=types.ReplyKeyboardRemove()
        )
