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


async def digipos_complain_choose_type_handler(dp, state_obj):
    user_form = state_obj['state']
    reset_proxy = state_obj['methods']['reset']
    default_proxy = state_obj['methods']['default']

    @dp.callback_query_handler(text='do_complain_question')  # if cb.data == 'no'
    @dp.callback_query_handler(text='do_complain_format')  # if cb.data == 'yes'
    async def handler(query: types.CallbackQuery, state: user_form):
        answer_data = query.data
        async with state.proxy() as proxy:
            # if not proxy.get('complain_digipos_detail'):
            #     return await query.message.answer(
            #         "Gagal, Ulangi Proses Komplain",
            #         reply_markup=types.ReplyKeyboardRemove()
            #     )
            if answer_data == 'do_complain_question':
                await default_proxy(proxy, addtions={
                    'complain_name': 'digipos'
                })
                await reset_proxy(proxy)
                proxy['complain_name'] = 'digipos'
                return await query.message.answer(
                    "Jelaskan Detail Komplain Digipos : ",
                    reply_markup=types.ReplyKeyboardRemove()
                )
            if answer_data == 'do_complain_format':
                return await query.message.answer(
                    "Bentar",
                    reply_markup=types.ReplyKeyboardRemove()
                )


async def digipos_complain_format_model_handler(message: types.Message, state, reset_proxy, default_proxy):
    from core import regex_special_character, is_registered, User
    from complain import upload_bukti_ask
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
            'complain_photo_require': False,
            'complain_photo': None,
            'complain_digipos_valid': None
        })
        # print(message.text)
        data: list = message.text.split('\n')
        search_data: list = message.text.lower().split('\n')
        pertanyaan: list = [
            'kabupaten',
            'kecamatan',
            'id outlet',
            'nama outlet',
            'no mkios',
            'no pelanggan',
            'tgl transaksi',
            'metode pembayaran',
            'versi apk digipos',
            'channel lain (umb)',
            'detil masalah'
        ]
        valid: list = []
        if not proxy['complain_digipos_valid']:
            for index, item in enumerate(data):
                if 'kabupaten :' in search_data[index]:
                    kabupaten = item.replace('Kabupaten : ', '')
                    if regex_special_character.search(kabupaten):
                        karakter = kabupaten[regex_special_character.search(kabupaten).span()[0]]
                        return await message.answer(f"Kabupaten tidak boleh memiliki special karakter {karakter}")
                    if len(kabupaten.strip()) > 149:
                        return await message.answer(f"Kabupaten tidak boleh lebih dari 149 karakter")
                    valid.append('kabupaten')
                    proxy["complain_digipos_kabupaten"] = kabupaten.strip().lower()
                if 'kecamatan :' in search_data[index]:
                    kecamatan = item.replace('Kecamatan : ', '')
                    if len(kecamatan.strip()) > 149:
                        return await message.answer(f"Kecamatan tidak boleh lebih dari 149 karakter")
                    valid.append('kecamatan')
                    proxy["complain_digipos_kecamatan"] = kecamatan.strip().lower()
                if 'id outlet :' in search_data[index]:
                    id_outlet = item.replace('ID Outlet : ', '')
                    if len(id_outlet.strip()) > 149:
                        return await message.answer(f"ID Outlet tidak boleh lebih dari 149 karakter")
                    valid.append('id outlet')
                    proxy["complain_digipos_id_outlet"] = id_outlet.strip()
                if 'nama outlet' in search_data[index]:
                    nama_oulet = item.replace('Nama Outlet : ', '')
                    if len(nama_oulet.strip()) > 149:
                        return await message.answer(f"Nama Outlet tidak boleh lebih dari 149 karakter")
                    valid.append('nama outlet')
                    proxy["complain_digipos_nama_outlet"] = nama_oulet.strip()
                if 'no mkios' in search_data[index]:
                    nomor_mkios = item.replace('No Mkios : ', '')
                    if len(nomor_mkios.strip()) > 29:
                        return await message.answer(f"Nomor MKios tidak boleh lebih dari 29 karakter")
                    try:
                        nomor_mkios = int(nomor_mkios.strip())
                    except:
                        return await message.answer("mkios harusnya berupa nomor")
                    valid.append('no mkios')
                    proxy["complain_digipos_no_mkios"] = nomor_mkios
                if 'no pelanggan' in search_data[index]:
                    no_pelanggan = item.replace('No Pelanggan : ', '')
                    if len(no_pelanggan.strip()) > 29:
                        return await message.answer(f"No Pelanggan tidak boleh lebih dari 29 karakter")
                    try:
                        no_pelanggan = int(no_pelanggan.strip())
                    except:
                        return await message.answer("No Pelanggan harusnya berupa nomor")
                    valid.append('no pelanggan')
                    proxy["complain_digipos_no_pelanggan"] = no_pelanggan
                if 'tgl transaksi :' in search_data[index]:
                    tgl_transaksi = item.replace('Tgl Transaksi : ', '')
                    if len(tgl_transaksi.strip()) > 149:
                        return await message.answer(f"Tgl Transaksi tidak boleh lebih dari 149 karakter")
                    valid.append('tgl transaksi')
                    proxy["complain_digipos_tgl_transaksi"] = tgl_transaksi.strip()
                if 'metode pembayaran :' in search_data[index]:
                    metode_pembayaran = item.replace('Metode Pembayaran : ', '')
                    if len(metode_pembayaran.strip()) > 149:
                        return await message.answer(f"Methode pembayaran tidak boleh lebih dari 149 karakter")
                    valid.append('metode pembayaran')
                    proxy["complain_digipos_pay_method"] = metode_pembayaran.strip()
                if 'versi apk digipos :' in search_data[index]:
                    versi_apk_digipos = item.replace('Versi APK DigiPos : ', '')
                    if len(versi_apk_digipos.strip()) > 149:
                        return await message.answer(f"Versi APK DigiPos tidak boleh lebih dari 149 karakter")
                    valid.append('versi apk digipos')
                    proxy["complain_digipos_versi_apk_dipos"] = versi_apk_digipos.strip()
                if 'channel lain (umb) :' in search_data[index]:
                    channel_lain_umb = item.replace('Channel lain (UMB) : ', '')
                    if len(channel_lain_umb.strip()) > 149:
                        return await message.answer(f"Channel lain (UMB) tidak boleh lebih dari 149 karakter")
                    valid.append('channel lain (umb)')
                    proxy["complain_digipos_channel_lain"] = channel_lain_umb.strip()
                if 'detil masalah :' in search_data[index]:
                    detil_masalah = item.replace('Detil Masalah : ', '')
                    if len(detil_masalah.strip()) > 149:
                        return await message.answer(f"Detil Masalah tidak boleh lebih dari 149 karakter")
                    valid.append('detil masalah')
                    proxy["complain_digipos_detail"] = detil_masalah.strip()
            proxy['complain_digipos_valid'] = 'harus_pilih_tombol'
            if pertanyaan == valid:
                return await upload_bukti_ask(message)
            return await message.answer(
                "GAGAL, harus ada spasi di antar titik dua `(:)` atau mungkin anda tidak memasukkan info yang lengkap",
                reply_markup=types.ReplyKeyboardRemove()
            )
        elif proxy['complain_digipos_valid'] == 'harus_pilih_tombol':
            return await message.answer(
                "[PERINGATAN] Pilih opsi !!",
                reply_markup=types.ReplyKeyboardRemove()
            )
        return await message.answer(
            "Terimakasih",
            reply_markup=types.ReplyKeyboardRemove()
        )


async def digipos_complain_question_model_handler(message: types.Message, state, reset_proxy, default_proxy):
    from complain import upload_bukti_ask, response_upload_bukti
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
            'complain_photo_require': False,
            'complain_photo': None,
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
                'menu': 'complain_photo',
                'pesan': upload_bukti_ask,
                'response': choose_menu_not_text
            }
        }

        # pencegahan
        if proxy['complain_photo_require']:
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


