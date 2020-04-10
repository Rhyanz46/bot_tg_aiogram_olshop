from aiogram import types
from core import goods, is_registered, User


async def do_buy(goods_selected, message, state):
    registered: User = await is_registered(message.from_user.id)
    if not registered.ok:
        return await message.reply("Kamu Belum Terdaftar 😝", reply_markup=types.ReplyKeyboardRemove())
    try:
        qty = int(message.text)
        async with state.proxy() as proxy:
            proxy['buy'] = {
                'buy': goods_selected,
                'qty': qty
            }
            proxy['do_verify_buy'] = True
            keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
            text_and_data = (
                ('Verifikasi Pembelian', 'verify_buy'),
                ('Cancel', 'cancel_buy'),
            )
            row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
            keyboard_markup.row(*row_btns)
            return await message.answer(f"Anda akan membeli {goods[goods_selected]} sebanyak {qty} "
                                        f"yang akan dikirim ke otlet {registered.nama_outlet}",
                                        reply_markup=keyboard_markup)
    except:
        async with state.proxy() as proxy:
            proxy['do_verify_buy'] = False
        return await message.answer(f"Gagal, masukkan jumlah dalam bentuk angka, ulangi lagi.",
                                    reply_markup=types.ReplyKeyboardRemove())


async def select_menu(message):
    if message.chat.type == 'group':
        return await message.answer(f"Perintah ini tidak berlaku disini, jika anda perlu bantuan saya, "
                                    f"Private Message ☺️")
    registered: User = await is_registered(message.from_user.id)
    if not registered.ok:
        return await message.reply("Kamu Belum Terdaftar 😝", reply_markup=types.ReplyKeyboardRemove())
    else:
        keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
        text_and_data = (
            (goods['buy_sp_reg'], 'buy_sp_reg'),
            (goods['buy_sp_data'], 'buy_sp_data'),
        )
        row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
        keyboard_markup.row(*row_btns)
        text_and_data = (
            (goods['voucher_fisik'], 'voucher_fisik'),
            (goods['linkaja'], 'linkaja'),
        )
        row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
        keyboard_markup.row(*row_btns)
        text_and_data = (
            (goods['mkios'], 'mkios'),
            (goods['bulk'], 'bulk'),
        )
        row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
        keyboard_markup.row(*row_btns)
        return await message.reply("Silahkan Dipilih Productnya", reply_markup=keyboard_markup)