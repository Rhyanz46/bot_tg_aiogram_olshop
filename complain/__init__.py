from aiogram import types


class Complain:
    def __init__(self, dp, state_obj):
        self.dp = dp
        self.state_obj = state_obj

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
        user_form = self.state_obj['state']
        reset_proxy = self.state_obj['methods']['reset']
        default_proxy = self.state_obj['methods']['default']

        @self.dp.callback_query_handler(text='digipos')  # if cb.data == 'no'
        @self.dp.callback_query_handler(text='voucher_fisik')  # if cb.data == 'yes'
        async def choose_complain_callback_handler(query: types.CallbackQuery, state: user_form):
            async with state.proxy() as proxy:
                await default_proxy(proxy)
                await reset_proxy(proxy)
                await default_proxy(proxy, addtions={
                    ''
                })

            answer_data = query.data
            if answer_data == 'digipos':
                return await query.message.answer(
                    "Cukup digipos",
                    reply_markup=types.ReplyKeyboardRemove()
                )
            return await query.message.answer(
                "Cukup voucer visik",
                reply_markup=types.ReplyKeyboardRemove()
            )
