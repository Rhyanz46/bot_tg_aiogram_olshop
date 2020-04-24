from core import (
    bot, dp, goods, is_registered,
    group_id, User, Order,
    order_barang, semua_produk_yg_ada_kategorinya,
    reset_proxy, default_proxy, complain,
    user_form, bot_name
)

from aiogram import executor, types
from daftar import formulir_daftar, daftar, menu
from buy import do_buy, select_product, temukan_nama_kategori_berdasarkan_kode_kat


class Opt:
    def __init__(self):
        pass


@dp.message_handler(commands='help')
async def help_cmd_handler(message: types.Message, state: user_form):
    async with state.proxy() as proxy:
        await default_proxy(proxy)
        await reset_proxy(proxy)
    keyboard_markup = types.ReplyKeyboardRemove()
    await message.answer("1.\tStart Bot\t\t\t\t\t\t\t\t\t\t\t\t: /start\n"
                         "2.\tDaftar\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t: /daftar\n"
                         "3.\tMenu\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t: /menu\n"
                         "4.\tBantuan Ini\t\t\t\t\t\t\t: /help", reply_markup=keyboard_markup)


@dp.message_handler(commands='Close!')
async def close_cmd_handler(message: types.Message):
    keyboard_markup = types.ReplyKeyboardRemove()
    await message.answer("Terimasih, untuk membuka menu lagi silahkan ketik : /menu atau /help", reply_markup=keyboard_markup)


@dp.message_handler(commands='menu')
async def menu_cmd_handler(message: types.Message, state: user_form):
    async with state.proxy() as proxy:
        await default_proxy(proxy)
        await reset_proxy(proxy)
    await menu(message)


@dp.message_handler(commands='daftar')
async def register_cmd_handler(message: types.Message):
    if message.chat.type == 'group':
        return await message.answer(f"Perintah ini tidak berlaku disini, jika anda perlu bantuan saya, "
                                    f"Private Message ☺️")
    await daftar(message)


@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message, state: user_form):
    async with state.proxy() as proxy:
        await default_proxy(proxy)
        if message.chat.type == 'group':
            if not proxy['joined']:
                proxy['joined'] = True
                return await message.answer(f"Terimakasih sudah memanggil saya, \n"
                                            f"mulai sekarang saya akan mengirim notifikasi kesini "
                                            f"jika seseorang meng-order barang, \n"
                                            f"jika anda perlu bantuan saya, "
                                            f"Private Message ☺️ jangan disini yaaa.")
            await reset_proxy(proxy, kecuali=['joined'])
            return await message.answer(f"Saya hanya mengirim notifikasi jika ada seseorang sedang "
                                        f"melakukan proses order, \n"
                                        f"jika anda perlu bantuan saya, "
                                        f"Private Message ☺️ jangan disini yaaa.")
        if not message.from_user.is_bot:
            await reset_proxy(proxy)
            # await reset_proxy(proxy, kecuali=['complain_chat_user_id_target'])
            # if proxy['complain_chat_user_id_target']:
            #     await message.answer(f"anda sekarang terhubung dengan ini orang")
            registered: User = await is_registered(message.from_user.id)
            if registered.ok:
                await message.answer(f"Ada yang bisa Kirana bantu? \n"
                                     f"Silakan ketik apa yang Anda inginkan.\n"
                                     f"Contoh : /help\n")
                await menu(message)
            else:
                keyboard_markup = types.ReplyKeyboardRemove()
                await message.answer(f"Selamat Datang {message.from_user.first_name} ☺️\n\n"
                                     f"Salam kenal aku {bot_name}. Selamat datang di Layanan Komplain Telkomsel Purwokerto "
                                     f"Raya ", reply_markup=keyboard_markup)
                await daftar(message)
        else:
            await message.answer("bot tidak di perbolehkan menggunakan ini , perlu bantuan? lakukakan perintah /help")


@dp.callback_query_handler(text='tolak_daftar')  # if cb.data == 'no'
@dp.callback_query_handler(text='daftar')  # if cb.data == 'yes'
async def register_answer_callback_handler(query: types.CallbackQuery):
    registered: User = await is_registered(query.from_user.id)
    if registered.ok:
        return await query.message.reply(f"Hello {query.from_user.first_name} "
                                         f"anda sudah terdaftar sebelumnya", reply_markup=types.ReplyKeyboardRemove())
    answer_data = query.data
    await query.answer(f'You answered with {answer_data!r}')
    if answer_data == 'daftar':
        await query.message.answer("untuk daftar balas pesan ini data dengan format seperti berikut",
                                   reply_markup=types.ReplyKeyboardRemove())
        await query.message.answer("#DAFTAR\n"
                                   "\nKabupaten : kabupaten kamu"
                                   "\nKecamatan :  kecamatan kamu"
                                   "\nNama Outlet :  nama outlet kamu"
                                   "\nNomor MKios : nomor mkios kamu")
        await query.message.answer("Contohnya : ")
        await query.message.answer("#DAFTAR\n"
                                   "\nKabupaten : Cilacap"
                                   "\nKecamatan : Cilacap Tengah"
                                   "\nNama Outlet : Yahya Cell"
                                   "\nNomor MKios : 081234567890")
    elif answer_data == 'tolak_daftar':
        keyboard_markup = types.ReplyKeyboardRemove()
        await bot.send_message(query.from_user.id, text=":( " ,reply_markup=keyboard_markup)
        text = 'jika anda berubah fikiran silahkan daftar dengan perintah /daftar atau /help'
        await bot.send_message(query.from_user.id, text)
    else:
        text = f'Unexpected callback data {answer_data!r}!'
        await bot.send_message(query.from_user.id, text)


@dp.callback_query_handler(text='verify_buy')  # if cb.data == 'yes'
@dp.callback_query_handler(text='cancel_buy')  # if cb.data == 'yes'
@dp.callback_query_handler(text='tambah_barang')  # if cb.data == 'yes'
async def verify_order_callback_handler(query: types.CallbackQuery, state: user_form):
    answer_data = query.data
    registered: User = await is_registered(query.from_user.id)
    if not registered.ok:
        return await query.message.reply("Sorry, Kamu Belum Terdaftar 😝", reply_markup=types.ReplyKeyboardRemove())
    async with state.proxy() as proxy:
        await default_proxy(proxy)
        if proxy.get('do_verify_buy') and proxy.get('buy'):
            if answer_data == 'verify_buy':
                admin_info = f"[PEMBELIAN] \n\n" \
                             f"----- Barang : \n"

                if not proxy['beli_banyak']:
                    if not proxy['buy'].get('kategori'):
                        admin_info += f"Barang : {goods[proxy['buy']['buy']]['nama']} \n" \
                                     f"Jumlah : {proxy['buy']['qty']} \n"
                    else:
                        kategori_name: str = temukan_nama_kategori_berdasarkan_kode_kat(proxy['buy']['buy'],
                                                                                        proxy['kategori'])
                        admin_info += f"nama = {goods[proxy['buy']['buy']]['nama']} \n" \
                                      f"Kategori = {kategori_name}\n" \
                                      f"Jumlah = {proxy['buy']['qty']} \n"
                else:
                    for item in proxy['beli_banyak']:
                        if not item.get('kategori'):
                            admin_info += f"\nNama : {goods[item['buy']]['nama']} \n" \
                                          f"Jumlah : {item['qty']} \n"
                        else:
                            kategori_name: str = temukan_nama_kategori_berdasarkan_kode_kat(item['buy'],
                                                                                            item['kategori'])
                            admin_info += f"\nnama = {goods[item['buy']]['nama']} \n" \
                                          f"Kategori = {kategori_name}\n" \
                                          f"Jumlah = {item['qty']} \n"
                    # get last data
                    if not proxy['buy'].get('kategori'):
                        admin_info += f"\nNama : {goods[proxy['buy']['buy']]['nama']} \n" \
                                     f"Jumlah : {proxy['buy']['qty']} \n"
                    else:
                        kategori_name: str = temukan_nama_kategori_berdasarkan_kode_kat(proxy['buy']['buy'],
                                                                                        proxy['kategori'])
                        admin_info += f"\nnama = {goods[proxy['buy']['buy']]['nama']} \n" \
                                      f"Kategori = {kategori_name}\n" \
                                      f"Jumlah = {proxy['buy']['qty']} \n"

                admin_info += f"\n\n----- Informasi User\n" \
                                 f"Nama User = {query.from_user.first_name} \n" \
                                 f"Nama Outlet = {registered.nama_outlet} \n" \
                                 f"Nomor MKios = {registered.nomor_mkios} \n" \
                                 f"Kabupaten = {registered.kabupaten} \n" \
                                 f"Kecamatan = {registered.kecamatan} \n" \
                                 f"\n\n" \
                                 f"---------"
                await bot.send_message(group_id, text=admin_info)
                order = Order()
                order.kode_barang = str(proxy['buy']['buy'])
                order.qty = proxy['buy']['qty']
                order.telegram_id = query.from_user.id
                # order.bot_message_id = query.message
                await order_barang(order)
                await reset_proxy(proxy)
                return await query.message.answer("Anda berhasil membeli", reply_markup=types.ReplyKeyboardRemove())
            elif answer_data == 'tambah_barang':
                if type(proxy['buy']) != dict:
                    await reset_proxy(proxy)
                    return await query.message.answer(
                        "Gagal, Ulangi Proses Order",
                        reply_markup=types.ReplyKeyboardRemove()
                    )
                await default_proxy(proxy)
                if proxy['beli_banyak']:
                    proxy['beli_banyak'].append(proxy['buy'])
                else:
                    proxy['beli_banyak'] = [proxy['buy']]
                await reset_proxy(proxy, kecuali=['beli_banyak'])
                return await query.message.answer("Silahkan Dipilih Lagi", reply_markup=types.ReplyKeyboardRemove())
                # return await select_menu(query.message)
            else:
                await reset_proxy(proxy)
                return await query.message.answer("Pembelian di cancel",
                                                 reply_markup=types.ReplyKeyboardRemove())
        return await query.message.answer("Tindakan anda ini tidak memverifikasi apapun, "
                                         "Perlu bantuan ? /help", reply_markup=types.ReplyKeyboardRemove())


@dp.callback_query_handler(text='as_5k')
@dp.callback_query_handler(text='simpati_10k')
@dp.callback_query_handler(text='loop_5k')
@dp.callback_query_handler(text='6/6.5gb')
@dp.callback_query_handler(text='7.5/8gb')
@dp.callback_query_handler(text='10gb')
@dp.callback_query_handler(text='4gb')
@dp.callback_query_handler(text='6.5gb')
@dp.callback_query_handler(text='8gb')
async def kategori_handler(query: types.CallbackQuery, state: user_form):
    if query.message.chat.type == 'group':
        return await query.message.answer(f"Perintah ini tidak berlaku disini, jika anda perlu bantuan saya, "
                                    f"Private Message ☺️")
    registered: User = await is_registered(query.from_user.id)
    if not registered.ok:
        await query.message.reply("Sorry, Kamu Belum Terdaftar 😝", reply_markup=types.ReplyKeyboardRemove())
    else:
        answer_data = query.data
        async with state.proxy() as proxy:  # proxy = FSMContextProxy(state); await proxy.load()
            if proxy['buy'] not in semua_produk_yg_ada_kategorinya():
                return await query.message.answer(
                    f"Perintah anda salah",
                    reply_markup=types.ReplyKeyboardRemove()
                )
            proxy['kategori'] = answer_data
            proxy['proses_beli'] = True
            kategori_name: str = temukan_nama_kategori_berdasarkan_kode_kat(proxy['buy'], answer_data)
            await query.message.answer(
                f"{goods[proxy['buy']]['nama']} | {kategori_name} \n"
                f"Masukkan jumlahnya barang dalam bentuk angka",
                reply_markup=types.ReplyKeyboardRemove()
            )


@dp.callback_query_handler(text='buy_sp_reg')  # if cb.data == 'no'
@dp.callback_query_handler(text='buy_sp_data')  # if cb.data == 'yes'
@dp.callback_query_handler(text='voucher_fisik')  # if cb.data == 'yes'
@dp.callback_query_handler(text='linkaja')  # if cb.data == 'yes'
@dp.callback_query_handler(text='mkios')  # if cb.data == 'yes'
@dp.callback_query_handler(text='bulk')  # if cb.data == 'yes'
async def order_callback_handler(query: types.CallbackQuery, state: user_form):
    if query.message.chat.type == 'group':
        return await query.message.answer(f"Perintah ini tidak berlaku disini, jika anda perlu bantuan saya, "
                                    f"Private Message ☺️")
    registered: User = await is_registered(query.from_user.id)
    if not registered.ok:
        await query.message.reply("Sorry, Kamu Belum Terdaftar 😝", reply_markup=types.ReplyKeyboardRemove())
    else:
        answer_data = query.data
        async with state.proxy() as proxy:  # proxy = FSMContextProxy(state); await proxy.load()
            await default_proxy(proxy)
            proxy['buy'] = answer_data
            proxy['do_verify_buy'] = True
            kategori = goods[answer_data].get('kategori')
            if kategori:
                proxy['harus_ada_kategori'] = True
                keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
                tombol = tuple([(item['nama'], item['kode']) for item in kategori])
                row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in tombol)
                keyboard_markup.row(*row_btns)
                return await query.message.answer(
                    f"Pilih Kategori dari {goods[answer_data]['nama']} : ",
                    reply_markup=keyboard_markup
                )
            else:
                async with state.proxy() as proxy:  # proxy = FSMContextProxy(state); await proxy.load()
                    await default_proxy(proxy)
                    proxy['proses_beli'] = True
                await query.answer(f'You answered with {goods[answer_data]["nama"]!r}')
                await query.message.answer(
                    f"Masukkan Jumlah {goods[answer_data]['nama']} yang ingin anda beli dalam bentuk angka",
                    reply_markup=types.ReplyKeyboardRemove()
                )


@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def photo_handler(message: types.Message, state: user_form):
    async with state.proxy() as proxy:
        if proxy.get('complain_photo_require'):
            from complain import response_upload_bukti
            return await response_upload_bukti(message, proxy)


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def all_message_handler(message: types.Message, state: user_form):
    async with state.proxy() as proxy:
        await default_proxy(proxy)
        if proxy.get('complain_name'):
            registered: User = await is_registered(message.from_user.id)
            if not registered.ok:
                return await message.reply("Sorry, Kamu Belum Terdaftar 😝", reply_markup=types.ReplyKeyboardRemove())
            return await complain.handle_message_complain(message, state, reset_proxy, default_proxy)
        if proxy['buy']:
            registered: User = await is_registered(message.from_user.id)
            if not registered.ok:
                return await message.reply("Sorry, Kamu Belum Terdaftar 😝", reply_markup=types.ReplyKeyboardRemove())
            elif proxy['harus_ada_kategori']:
                if proxy['kategori']:
                    return await do_buy(proxy['buy'], message, state)
                await reset_proxy(proxy)
            else:
                if type(proxy['buy']) != str:
                    await reset_proxy(proxy)
                    return await message.answer(
                        "Maaf, Terjadi kesalahan, Ulangi pembelian di perintah /menu",
                        reply_markup=types.ReplyKeyboardRemove()
                    )
                return await do_buy(proxy['buy'], message, state)
        else:
            async with state.proxy() as proxy:
                proxy.setdefault('buy', 0)
        if message.chat.type == 'group':
            print(message)
            return await message.answer(
                f"Perintah ini tidak berlaku disini, jika anda perlu bantuan saya, "
                f"Private Message ☺️"
            )
        if '#DAFTAR\n' and 'Kabupaten' and 'Kecamatan' and 'Nama Outlet' and 'Nomor MKios' in message.text:
            return await formulir_daftar(message)
        if message.text == "(_Belanja_)":
            async with state.proxy() as proxy:
                await default_proxy(proxy)
                await reset_proxy(proxy)
            return await select_product(message)
        if message.text == "(_Komplain_)":
            async with state.proxy() as proxy:
                await default_proxy(proxy)
                await reset_proxy(proxy)
            registered: User = await is_registered(message.from_user.id)
            if not registered.ok:
                return await message.reply(
                    "Sorry, Kamu Belum Terdaftar 😝",
                    reply_markup=types.ReplyKeyboardRemove()
                )
            return await complain.choose_complain_menu(message)
        return await message.answer(
            f"Ada yang bisa dibantu {message.from_user.first_name}? Ketik ini ya /help",
            reply_markup=types.ReplyKeyboardRemove()
        )


if __name__ == '__main__':
    import sentry_sdk
    sentry_sdk.init("https://8d4c913cbef54ec4a8b8364f8f2c7fd7@o382669.ingest.sentry.io/5211893")
    executor.start_polling(dp, skip_updates=False)
