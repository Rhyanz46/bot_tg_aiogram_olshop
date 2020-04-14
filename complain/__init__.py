from aiogram import types
from complain.digipos import digipos_complain_handler


class Complain:
    def __init__(self, dp, state_obj):
        self.dp = dp
        self.state_obj = state_obj

    async def load(self):
        await self.choose_complain_handler()

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
                    "Cukup digipos",
                    reply_markup=types.ReplyKeyboardRemove()
                )
            return await query.message.answer(
                "Cukup voucer visik",
                reply_markup=types.ReplyKeyboardRemove()
            )
