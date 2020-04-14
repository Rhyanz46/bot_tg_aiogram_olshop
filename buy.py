from aiogram import types
from core import goods, is_registered, User, reset_proxy, default_proxy


def temukan_nama_kategori_berdasarkan_kode_kat(barang, kode) -> str:
    for item in goods[barang]['kategori']:
        if item['kode'] == kode:
            return item['nama']
    return ''


async def do_buy(goods_selected, message, state):
    registered: User = await is_registered(message.from_user.id)
    if not registered.ok:
        return await message.reply("Kamu Belum Terdaftar 😝", reply_markup=types.ReplyKeyboardRemove())

    try:
        qty = int(message.text)
    except:
        async with state.proxy() as proxy:
            await default_proxy(proxy)
            proxy['do_verify_buy'] = False
        return await message.answer(f"Gagal, masukkan jumlah dalam bentuk angka, ulangi lagi.",
                                    reply_markup=types.ReplyKeyboardRemove())
    async with state.proxy() as proxy:
        await default_proxy(proxy)
        proxy['buy'] = {
            'buy': goods_selected,
            'qty': qty
        }
        proxy['do_verify_buy'] = True
        keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
        text_and_data = (
            ('Order Ini Aja', 'verify_buy'),
            ('Tambah Lagi', 'tambah_barang'),
            ('Cancel', 'cancel_buy'),
        )
        row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
        keyboard_markup.row(*row_btns)
        if proxy['kategori']:
            proxy['buy'] = {
                'buy': goods_selected,
                'qty': qty,
                'kategori': proxy['kategori']
            }
            kategori_name: str = temukan_nama_kategori_berdasarkan_kode_kat(goods_selected, proxy['kategori'])
            return await message.answer(f"Anda akan membeli {goods[goods_selected]['nama']} dengan kategory "
                                        f"{kategori_name} sebanyak {qty} "
                                        f"yang akan dikirim ke otlet {registered.nama_outlet}",
                                        reply_markup=keyboard_markup)
        return await message.answer(f"Anda akan membeli {goods[goods_selected]['nama']} sebanyak {qty} "
                                    f"yang akan dikirim ke otlet {registered.nama_outlet}",
                                    reply_markup=keyboard_markup)


async def select_product(message):
    if message.chat.type == 'group':
        return await message.answer(f"Perintah ini tidak berlaku disini, jika anda perlu bantuan saya, "
                                    f"Private Message ☺️")
    registered: User = await is_registered(message.from_user.id)
    if not registered.ok:
        return await message.reply("Kamu Belum Terdaftar 😝", reply_markup=types.ReplyKeyboardRemove())
    else:
        keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
        text_and_data = (
            (goods['buy_sp_reg']['nama'], 'buy_sp_reg'),
            (goods['buy_sp_data']['nama'], 'buy_sp_data'),
        )
        row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
        keyboard_markup.row(*row_btns)
        text_and_data = (
            (goods['voucher_fisik']['nama'], 'voucher_fisik'),
            (goods['linkaja']['nama'], 'linkaja'),
        )
        row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
        keyboard_markup.row(*row_btns)
        text_and_data = (
            (goods['mkios']['nama'], 'mkios'),
            (goods['bulk']['nama'], 'bulk'),
        )
        row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
        keyboard_markup.row(*row_btns)
        return await message.reply("Silahkan Dipilih Productnya", reply_markup=keyboard_markup)