from aiogram import types


class Complain:
    def __init__(self, dp):
        self.dp = dp

    async def load(self):
        await self.choose_complain_handler()

    @staticmethod
    async def choose_complain(message: types.Message):
        keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
        text_and_data = (
            ('Komplain Digipos', 'digipos'),
            ('Komplain Voucer Fisik', 'voucher_fisik'),
        )
        row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
        keyboard_markup.row(*row_btns)
        await message.reply("Pilih", reply_markup=keyboard_markup)

    async def choose_complain_handler(self):
        @self.dp.callback_query_handler(text='digipos')  # if cb.data == 'no'
        @self.dp.callback_query_handler(text='voucher_fisik')  # if cb.data == 'yes'
        async def choose_complain_callback_handler(query: types.CallbackQuery):
            return await query.message.answer("Cukup roma")
