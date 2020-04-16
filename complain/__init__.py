from aiogram import types
import time
from uuid import uuid4
from complain.digipos import digipos_complain_handler, digipos_complain_confirmation_handler


class Complain:
    def __init__(self, dp, state_obj):
        self.complain = None
        self.dp = dp
        self.state_obj = state_obj

    async def load(self):
        await self.choose_complain_handler()
        await digipos_complain_confirmation_handler(self.dp, self.state_obj)

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
            "Pilih",
            reply_markup=keyboard_markup
        )

    async def send(self, query, state):
        from core import bot, group_id
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
        text = f"Pelaporan Kendala Transaksi {self.complain['type']}\n\n" \
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
               f"Type : DigiPos"

        keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
        text_and_data = (
            ('Beri Response', 'complain_response'),
        )
        row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
        keyboard_markup.row(*row_btns)
        aa = await bot.send_message(group_id, text=text, reply_markup=keyboard_markup)
        # print(aa)
        # print(registered, registered.telegram_id)
        await query.message.answer(
            "Tunggu Sebentar . . . ",
            reply_markup=types.ReplyKeyboardRemove()
        )
        time.sleep(2)
        return await query.message.answer(
            f"Teriamakasih, komplain {self.complain['type']} anda berhasil di kirim, tunggu response 1x24 jam :) \n\n\n"
            f"Complain Id : {complain_id}",
            reply_markup=types.ReplyKeyboardRemove()
        )

    @staticmethod
    async def handle_message_complain(message: types.Message, state, reset_proxy, default_proxy):
        async with state.proxy() as proxy:
            if proxy['complain_name'] == 'digipos':
                return await digipos_complain_handler(message, state, reset_proxy, default_proxy)
            if proxy['complain_name'] == 'voucher_fisik':
                return await message.answer('on development...')

    async def choose_complain_handler(self):
        user_form = self.state_obj['state']
        reset_proxy = self.state_obj['methods']['reset']
        default_proxy = self.state_obj['methods']['default']

        @self.dp.callback_query_handler(text='complain_response')  # if cb.data == 'no'
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
                return await query.message.answer(
                    "Jelaskan Detail Komplain Digipos : ",
                    reply_markup=types.ReplyKeyboardRemove()
                )
            if answer_data == 'complain_response':
                # breakpoint()
                return await query.message.answer(
                    "Digidaw",
                    reply_markup=types.ReplyKeyboardRemove()
                )
            return await query.message.answer(
                "Jelaskan Detail Komplain Voucer Fisik : ",
                reply_markup=types.ReplyKeyboardRemove()
            )
