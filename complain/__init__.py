from aiogram import types
from aiogram.utils import exceptions
import time
from uuid import uuid4
import re
from complain.digipos import digipos_complain_format_model_handler
from complain.voucer_fisik import voucer_fisik_complain_format_model_handler


async def upload_bukti_ask(message, position=None, state=None, reset_proxy=None, default_proxy=None):
    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    text_and_data = (
        ('Upload Foto Bukti', 'req_photo_complain'),
        ('Tidak', 'no_req_photo_complain'),
    )
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
    keyboard_markup.row(*row_btns)
    return await message.answer(
        "Kalau kamu punya bukti berupa screenshoot atau foto, tolong diupload ya biar Kirana mudah check kendalamu",
        reply_markup=keyboard_markup
    )


async def send_complain_or_not(message: types.Message, proxy):
    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    text_and_data = (
        ('Tambah Foto Bukti', 'req_photo_complain'),
    )
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
    keyboard_markup.row(*row_btns)
    text_and_data = (
        ('Kirim Komplain', 'ya_complain'),
        ('BATAL', 'batal_complain'),
    )
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
    keyboard_markup.row(*row_btns)
    return await message.answer(
        "Kamu udah yakin ya dengan komplain dan buktinya? Kalau udah klik kirim komplain",
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
    if not proxy['complain_photo']:
        proxy['complain_photo'] = [message.photo[-1].file_id]
    else:
        proxy['complain_photo'].append(message.photo[-1].file_id)
    await message.answer(
        "Dengan bukti yang kamu kirim ini akan membuat kirana mudah dalam proses peninjauan",
        reply_markup=types.ReplyKeyboardRemove()
    )
    # sleep(2)
    proxy['complain_photo_require'] = False
    await send_complain_or_not(message, proxy)


class Complain:
    def __init__(self, dp, state_obj):
        self.complain = None
        self.dp = dp
        self.state_obj = state_obj

    async def load(self):
        await self.choose_complain_handler()
        await self.complain_confirmation_handler()
        await self.photo_complain_handler()

    async def photo_complain_handler(self):
        user_form = self.state_obj['state']
        reset_proxy = self.state_obj['methods']['reset']
        default_proxy = self.state_obj['methods']['default']

        @self.dp.callback_query_handler(text='req_photo_complain')  # if cb.data == 'no'
        @self.dp.callback_query_handler(text='no_req_photo_complain')  # if cb.data == 'no'
        async def handler(query: types.CallbackQuery, state: user_form):
            from complain import send_complain_or_not
            answer_data = query.data
            async with state.proxy() as proxy:
                if not proxy.get('complain_name'):
                    await default_proxy(proxy)
                    await reset_proxy(proxy)
                    return await query.message.answer(
                        "Gagal, Ulangi Proses Komplain",
                        reply_markup=types.ReplyKeyboardRemove()
                    )
                if answer_data == 'req_photo_complain':
                    proxy['complain_photo_require'] = True
                    return await query.message.answer(
                        "Silahkan upload gambar kesini.",
                        reply_markup=types.ReplyKeyboardRemove()
                    )
                if answer_data == 'no_req_photo_complain':
                    await query.message.answer(
                        "Tidak perlu khawatir jika anda tidak memiliki bukti, kami akan berusaha meninjaunya",
                        reply_markup=types.ReplyKeyboardRemove()
                    )
                    await send_complain_or_not(query.message, proxy)

    async def complain_confirmation_handler(self):
        user_form = self.state_obj['state']
        reset_proxy = self.state_obj['methods']['reset']
        default_proxy = self.state_obj['methods']['default']

        @self.dp.callback_query_handler(text='ya_complain')  # if cb.data == 'no'
        @self.dp.callback_query_handler(text='batal_complain')  # if cb.data == 'yes'
        async def handler(query: types.CallbackQuery, state: user_form):
            answer_data = query.data
            async with state.proxy() as proxy:
                if not proxy.get('complain_name'):
                    await default_proxy(proxy)
                    await reset_proxy(proxy)
                    return await query.message.answer(
                        "Gagal, Ulangi Proses Komplain",
                        reply_markup=types.ReplyKeyboardRemove()
                    )
                if answer_data == 'batal_complain':
                    await reset_proxy(proxy)
                    return await query.message.answer(
                        "Anda telah membatalkan proses complain",
                        reply_markup=types.ReplyKeyboardRemove()
                    )
                if answer_data == 'ya_complain':
                    from core import complain
                    if proxy['complain_name'] == 'digipos':
                        complain.complain = {
                            'type': proxy['complain_name'],
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
                            'photo': proxy['complain_photo']
                        }
                        return await complain.send(query, state)
                    if proxy['complain_name'] == 'voucher_fisik':
                        complain.complain = {
                            'type': proxy['complain_name'],
                            'kabupaten': proxy['complain_vf_kabupaten'],
                            'kecamatan': proxy['complain_vf_kecamatan'],
                            'nama_outlet': proxy['complain_vf_nama_outlet'],
                            'id_digipos_outlet': proxy['complain_vf_id_digipos_outlet'],
                            'nomor_pelanggan': proxy['complain_vf_nomor_pelanggan'],
                            'serial_number': proxy['complain_vf_serial_number'],
                            'tgl_inject_voucher': proxy['complain_vf_tgl_inject_voucher'],
                            'paket': proxy['complain_vf_paket'],
                            'masalah': proxy['complain_vf_masalah'],
                            'photo': proxy['complain_photo']
                        }
                        return await complain.send(query, state)

    @staticmethod
    async def choose_complain_menu(message: types.Message):
        keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
        text_and_data = (
            ('Komplain Digipos', 'digipos'),
            ('Komplain Voucer Fisik', 'voucher_fisik'),
        )
        row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
        keyboard_markup.row(*row_btns)
        await message.reply(
            "Pilih salah satu ya.. nanti Kirana bantu",
            reply_markup=keyboard_markup
        )

    async def send(self, query, state):
        from core import bot, group_id, ComplainDigiposData, ComplainVoucherFisikData

        complain_id = str(uuid4())
        registered = await self.state_obj['query']['is_registered'](query.from_user.id)

        if not registered.ok:
            await query.message.answer(
                "Daftar Dulu dong. . . ",
                reply_markup=types.ReplyKeyboardRemove()
            )

        reset_proxy = self.state_obj['methods']['reset']
        async with state.proxy() as proxy:
            await reset_proxy(proxy)
        if self.complain['type'] == 'digipos':
            text = f"Pelaporan Kendala Transaksi DigiPos\n\n" \
                   f"Kabupaten : {self.complain['kabupaten']}\n" \
                   f"Kecamatan : {self.complain['kecamatan']}\n" \
                   f"ID Outlet : {self.complain['id_outlet']}\n" \
                   f"Nama Outlet : {self.complain['nama_outlet']}\n" \
                   f"No Mkios : {self.complain['no_mkios']}\n" \
                   f"No Pelanggan : {self.complain['no_pelanggan']}\n" \
                   f"Tgl Transaksi : {self.complain['tgl_transaksi']}\n" \
                   f"Metode Pembayaran : {self.complain['pay_method']}\n" \
                   f"Versi APK DigiPos : {self.complain['versi_apk_dipos']}\n" \
                   f"Channel lain (UMB) : {self.complain['channel_lain']}\n" \
                   f"Detil Masalah : {self.complain['detail']}\n\n\n" \
                   f"Complain ID : {complain_id}\n" \
                   f"User First Name : {query.from_user.first_name}\n" \
                   f"User Id : {registered.telegram_id} \n" \
                   f"Type : DigiPos"
            # save to database
            ComplainDigiposData(complain_id).new(
                self.complain,
                registered.telegram_id,
                complain_type='digipos',
                chat_id=query.message.chat.id,
                message_id=query.message.message_id
            )
            # end save to database
        else:  # voucher fisik
            text = f"Pelaporan Kendala Transaksi Voucher Fisik\n\n" \
                   f"Kabupaten : {self.complain['kabupaten']}\n" \
                   f"Kecamatan : {self.complain['kecamatan']}\n" \
                   f"Nama Outlet : {self.complain['nama_outlet']}\n" \
                   f"ID Digipos Outlet : {self.complain['id_digipos_outlet']}\n" \
                   f"Nomor Pelanggan : {self.complain['nomor_pelanggan']}\n" \
                   f"Serial Number : {self.complain['serial_number']}\n" \
                   f"Tanggal Inject Voucher : {self.complain['tgl_inject_voucher']}\n" \
                   f"Paket : {self.complain['paket']}\n" \
                   f"Masalah : {self.complain['masalah']}\n\n\n" \
                   f"Complain ID : {complain_id}\n" \
                   f"User First Name : {query.from_user.first_name}\n" \
                   f"User Id : {registered.telegram_id} \n" \
                   f"Type : Voucher Fisik"
            ComplainVoucherFisikData(complain_id).new(
                self.complain,
                registered.telegram_id,
                complain_type='voucher_fisik',
                chat_id=query.message.chat.id,
                message_id=query.message.message_id
            )
        keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
        text_and_data = (
            ('Proses', 'complain_response_responded'),
        )
        row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
        keyboard_markup.row(*row_btns)
        try:
            aa = await bot.send_message(group_id, text=text, reply_markup=keyboard_markup)
        except exceptions.ChatNotFound:
            raise exceptions.ChatNotFound("Akses ke grup belum ada")

        if self.complain['photo']:
            for item in self.complain['photo']:
                await bot.send_photo(group_id, item, reply_to_message_id=aa.message_id)

        await query.message.answer(
            "Tunggu Sebentar . . . ",
            reply_markup=types.ReplyKeyboardRemove()
        )

        time.sleep(1.5)
        return await query.message.answer(
            f"Terimakasih {query.from_user.first_name}, komplain {self.complain['type']} berhasil dikirim, tunggu response Kirana 1x24jam ya\n\n"
            f"Ohya user telegram kamu jangan diprivate ya biar nanti Kirana chat kamu\n\n"
            f"Complain Id : {complain_id}",
            reply_markup=types.ReplyKeyboardRemove()
        )

    @staticmethod
    async def handle_message_complain(message: types.Message, state, reset_proxy, default_proxy):
        async with state.proxy() as proxy:
            if proxy['complain_name'] == 'digipos':
                return await digipos_complain_format_model_handler(message, state, reset_proxy, default_proxy)
            if proxy['complain_name'] == 'voucher_fisik':
                return await voucer_fisik_complain_format_model_handler(message, state, reset_proxy, default_proxy)

    async def choose_complain_handler(self):
        user_form = self.state_obj['state']
        reset_proxy = self.state_obj['methods']['reset']
        default_proxy = self.state_obj['methods']['default']

        @self.dp.callback_query_handler(text='complain_response_responded')
        @self.dp.callback_query_handler(text='open_chat')  # if cb.data == 'no'
        @self.dp.callback_query_handler(text='digipos')  # if cb.data == 'no'
        @self.dp.callback_query_handler(text='voucher_fisik')  # if cb.data == 'yes'
        async def choose_complain_callback_handler(query: types.CallbackQuery, state: user_form):
            answer_data = query.data
            async with state.proxy() as proxy:
                await default_proxy(proxy, addtions={
                    'complain_name': answer_data
                })
                await reset_proxy(proxy)
                proxy['complain_name'] = answer_data
            if answer_data == 'digipos':
                await query.message.answer(
                    "Kirim complain kesini dalam bentuk format berikut : \n\n",
                    reply_markup=types.ReplyKeyboardRemove()
                )
                await query.message.answer(
                    "Kabupaten : Kabupaten Anda\n"
                    "Kecamatan : Kecamatan Anda\n"
                    "ID Outlet : no outlet anda\n"
                    "Nama Outlet : nama otlet\n"
                    "No Mkios : no mkios\n"
                    "No Pelanggan : no handphone\n"
                    "Tgl Transaksi : waktu transaksi\n"
                    "Metode Pembayaran : metode pembayawran\n"
                    "Versi APK DigiPos : versi apk\n"
                    "Channel lain (UMB) : channel lain\n"
                    "Detil Masalah : Tulis masalah anda disini",
                    reply_markup=types.ReplyKeyboardRemove()
                )
                return await query.message.answer(
                    "Contoh pengisiannya :\n\n"
                    "Kabupaten : Cilacap atau kabupaten kamu domisili\n"
                    "Kecamatan : Cilacap Tengah atau kabupaten kamu domisili\n"
                    "ID Outlet : 31000XXXX atau biasanya 10 angka tanya Sales dulu ya\n"
                    "Nama Outlet : xxx Cell atau nama Kontermu ya\n"
                    "No Mkios : 081234XXXXXX atau biasanya 11-12 angka\n"
                    "No Pelanggan : 081234XXXXXX atau biasanya 11-12 angka kalau tidak ada diisi angka 0 aja ya\n"
                    "Tgl Transaksi : 23/04/2020 atau tanggal transaksinya ya\n"
                    "Metode Pembayaran : Linkaja atau NGRS, coba pilih salah satu\n"
                    "Versi APK DigiPos : .84 kalau semisal pakai aplikasi Digipos kalau tidak pakai diisi angka 0 aja ya\n"
                    "Channel lain (UMB) : UMB 181 kalau semisal pakai UMB\n"
                    "Detil Masalah :\n"
                    "Ceritain kendalamu contohnya kayak gini\n\n"
                    "- Transaksi `Dalam Proses` lebih dari 1x24jam, saldo sudah terpotong\n"
                    "- Transaksi `Gagal`, saldo sudah terpotong namun saldo belum kembali\n"
                    "- Transaksi `Sukses`, Saldo sudah terpotong namun kuota belum masuk\n"
                    "- Transaksi `Sekali` tapi motong Saldo `Dua Kali`\n"
                    "- Atau ceritain kendalamu ya",
                    reply_markup=types.ReplyKeyboardRemove()
                )
            if answer_data == 'voucher_fisik':
                await query.message.answer(
                    "Kirim complain kesini dalam bentuk format berikut : \n\n",
                    reply_markup=types.ReplyKeyboardRemove()
                )
                await query.message.answer(
                    "Kabupaten : Kabupaten Anda\n"
                    "Kecamatan : Kecamatan Anda\n"
                    "Nama Outlet : nama otlet\n"
                    "ID Digipos Outlet : no outlet anda\n"
                    "Nomor Pelanggan : no handphone\n"
                    "Serial Number (12Digit) : 1222222\n"
                    "Tanggal Inject Voucher : 1-4-2020\n"
                    "Paket : 4GB\n"
                    "Masalah : Voucher Internet Fisik inject berhasil "
                    "Kuota 1gb lokal tidak dapat digunakan\n",
                    reply_markup=types.ReplyKeyboardRemove()
                )
                return await query.message.answer(
                    "Contoh pengisiannya\n\n"
                    "Kabupaten : Cilacap atau kabupaten kamu domisili\n"
                    "Kecamatan : Cilacap Tengah atau kabupaten kamu domisili\n"
                    "Nama Outlet : xxx Cell atau nama Kontermu ya\n"
                    "ID Digipos Outlet : 31000XXXX atau biasanya 10 angka tanya Sales dulu ya\n"
                    "Nomor Pelanggan : 081234XXXXXX atau biasanya 11-12 angka kalau tidak ada diisi angka 0 aja ya\n"
                    "Serial Number (12Digit) : 9000 XXXX XXXX atau bisa liat nomor di belakang voucher ya\n"
                    "Tanggal Inject Voucher : 23/04/2020 atau tanggal injectnya ya\n"
                    "Paket : 4GB/6.5GB/8GB\n"
                    "Detil Masalah :\n\n "
                    "Ceritain kendalamu contohnya kayak gini :\n"
                    "- Voucher Fisik inject Berhasil, Kuota Lokal tidak dapat digunakan\n"
                    "- Voucher Fisik inject Berhasil, Kuota tidak masuk, cek *132# voucher sudah terpakai\n"
                    "- Cek Kuota VF dan *132# tidak ada balasan atau balasannya NOK:ProductNotAvailable\n"
                    "- Cek Regional anda padahal pelanggan ada dikonter"
                )
            if answer_data == 'complain_response_responded':
                # asisten_arian_bot
                from core import bot, ComplainDigiposData, ComplainVoucherFisikData
                index_complain_id = query.message.text.find('\nComplain ID : ')
                index_user_id = query.message.text.find('\nUser Id')
                index_complain_type = query.message.text.find('\nType')
                user_telegram_id = int(re.search(r'\d+', query.message.text[index_user_id:]).group())
                complain_id = query.message.text[index_complain_id:].split('\n')[1].split('Complain ID : ')[1]
                complain_type = query.message.text[index_complain_type:].split('\n')[1].split('Type : ')[1].lower()

                if complain_type == 'digipos':
                    complain = ComplainDigiposData(complain_id).get()
                else:  # Voucher Fisik
                    complain = ComplainVoucherFisikData(complain_id).get()

                user_complain = await bot.get_chat(complain.telegram_id)
                if complain.telegram_id == query.from_user.id:
                    return await query.answer("Anda tidak bisa meresponse komplainan anda sendiri")
                if complain.status == 'unprogress':
                    # async with state.proxy() as proxy:
                    #     await default_proxy(proxy)
                    #     await reset_proxy(proxy)
                    #     proxy['complain_chat_user_id_target'] = str(user_complain.id)
                    complain.set_status('onprogress', admin_id=query.from_user.id)
                    # edit button
                    if user_complain.username:
                        keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
                        text_and_data = (
                            ('Interaksi Langsung', f'https://t.me/{user_complain.username}'),
                        )

                        row_btns = (types.InlineKeyboardButton(text, url=data) for text, data in text_and_data)
                        keyboard_markup.row(*row_btns)
                        await bot.edit_message_reply_markup(
                            chat_id=query.message.chat.id,
                            message_id=query.message.message_id,
                            reply_markup=keyboard_markup
                        )
                    else:
                        return await query.message.answer(
                            "Privasi user tidak di buka, jadi tidak bisa interaksi langsung, \n"
                            f"complain id: {complain_id}"
                        )

                await bot.send_message(
                    user_telegram_id,
                    f"Komplain Anda Sedang di Tinjau Oleh Admin : {query.from_user.first_name}."
                )
                admin_detail = await bot.get_chat(complain.handler_user_id)
                return await query.answer(f'Komplain ini sudah di tangani sebelumnya oleh {admin_detail.first_name}')
