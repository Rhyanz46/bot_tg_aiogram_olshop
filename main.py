from core import bot, dp, goods, is_registered, group_id, User, Order, order_barang, semua_produk_yg_ada_kategorinya
from aiogram import executor, types
from daftar import formulir_daftar, daftar, menu
from buy import do_buy, select_menu, temukan_nama_kategori_berdasarkan_kode_kat

from aiogram.dispatcher.filters.state import State, StatesGroup


class UserForm(StatesGroup):
    name = State()  # Will be represented in storage as 'Form:name'
    age = State()  # Will be represented in storage as 'Form:age'
    gender = State()  # Will be represented in storage as 'Form:gender'


user_form = UserForm()


@dp.message_handler(commands='help')
async def help_cmd_handler(message: types.Message):
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
async def menu_cmd_handler(message: types.Message):
    await menu(message)


@dp.message_handler(commands='daftar')
async def register_cmd_handler(message: types.Message):
    if message.chat.type == 'group':
        return await message.answer(f"Perintah ini tidak berlaku disini, jika anda perlu bantuan saya, "
                                    f"Private Message ☺️")
    await daftar(message)


@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message, state: user_form):
    if message.chat.type == 'group':
        async with state.proxy() as proxy:
            proxy.setdefault('joined', False)
            if not proxy['joined']:
                proxy['joined'] = True
                return await message.answer(f"Terimakasih sudah memanggil saya, "
                                            f"saya akan mengirim notifikasi kesini "
                                            f"jika seseorang meng-order barang, "
                                            f"jika anda perlu bantuan saya, "
                                            f"Private Message ☺️ jangan disini yaaa.")
            return await message.answer(f"Saya hanya mengirim notifikasi jika ada seseorang sedang "
                                        f"melakukan proses order "
                                        f"jika anda perlu bantuan saya, "
                                        f"Private Message ☺️ jangan disini yaaa.")
    if not message.from_user.is_bot:
        registered: User = await is_registered(message.from_user.id)
        if registered.ok:
            await message.answer(f"selamat datang kembali "
                                 f"{message.from_user['first_name']} ☺️"
                                 f", perlu bantuan? lakukan perintah /help ")
            await menu(message)
        else:
            keyboard_markup = types.ReplyKeyboardRemove()
            await message.answer(f"Selamat Datang {message.from_user.first_name} ☺️",reply_markup=keyboard_markup)
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
        if proxy['do_verify_buy'] and proxy['buy']:
            if answer_data == 'verify_buy':
                await bot.send_message(group_id, text=f"[PEMBELIAN] \n\n"
                                                      f"Barang : {goods[proxy['buy']['buy']]['nama']} \n"
                                                      f"Jumlah : {proxy['buy']['qty']} \n\n"
                                                      f"Nama User : {query.from_user.first_name} \n"
                                                      f"Nama Outlet : {registered.nama_outlet} \n"
                                                      f"Nomor MKios : {registered.nomor_mkios} \n"
                                                      f"Kabupaten : {registered.kabupaten} \n"
                                                      f"Kecamatan : {registered.kecamatan} \n"
                                                      f"\n\n"
                                                      f"---------")
                order = Order()
                order.kode_barang = str(proxy['buy']['buy'])
                order.qty = proxy['buy']['qty']
                order.telegram_id = query.from_user.id
                # order.bot_message_id = query.message
                await order_barang(order)

                proxy['buy'] = False
                proxy['do_verify_buy'] = False
                proxy['proses_beli'] = False
                proxy['kategori'] = False
                proxy['harus_ada_kategori'] = False
                return await query.message.answer("Anda berhasil membeli", reply_markup=types.ReplyKeyboardRemove())
            elif answer_data == 'tambah_barang':
                proxy['buy'] = False
                proxy['do_verify_buy'] = False
                proxy['proses_beli'] = False
                proxy['kategori'] = False
                proxy['harus_ada_kategori'] = False
                return await query.message.answer("Ettt Belum jahaddddi", reply_markup=types.ReplyKeyboardRemove())
            else:
                proxy['buy'] = False
                proxy['do_verify_buy'] = False
                proxy['proses_beli'] = False
                proxy['kategori'] = False
                proxy['harus_ada_kategori'] = False
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
            proxy['buy'] = answer_data
            proxy['do_verify_buy'] = True
            print('proxy | order_callback_handler')
            print(proxy)
            print('proxy | order_callback_handler')
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
                    proxy['proses_beli'] = True
                await query.answer(f'You answered with {goods[answer_data]["nama"]!r}')
                await query.message.answer(
                    f"Masukkan Jumlah {goods[answer_data]['nama']} yang ingin anda beli dalam bentuk angka",
                    reply_markup=types.ReplyKeyboardRemove()
                )


@dp.message_handler()
async def all_message_handler(message: types.Message, state: user_form):
    async with state.proxy() as proxy:
        proxy.setdefault('buy', 0)
        proxy.setdefault('do_verify_buy', 0)
        proxy.setdefault('proses_beli', 0)
        proxy.setdefault('kategori', 0)
        proxy.setdefault('harus_ada_kategori', 0)
        print('proxy | all_message_handler')
        print(proxy)
        print('proxy | all_message_handler')
        if proxy['buy']:
            registered: User = await is_registered(message.from_user.id)
            if not registered.ok:
                return await message.reply("Sorry, Kamu Belum Terdaftar 😝", reply_markup=types.ReplyKeyboardRemove())
            elif proxy['harus_ada_kategori']:
                if proxy['kategori']:
                    return await do_buy(proxy['buy'], message, state)
                return await message.reply("Pilih Kategori Terlebih Dahulu", reply_markup=types.ReplyKeyboardRemove())
            else:
                return await do_buy(proxy['buy'], message, state)
        else:
            async with state.proxy() as proxy:
                proxy.setdefault('buy', 0)
        if message.chat.type == 'group':
            return await message.answer(f"Perintah ini tidak berlaku disini, jika anda perlu bantuan saya, "
                                        f"Private Message ☺️")
        if '#DAFTAR\n' and 'Kabupaten' and 'Kecamatan' and 'Nama Outlet' and 'Nomor MKios' in message.text:
            return await formulir_daftar(message)
        if message.text == "(_Belanja_)":
            return await select_menu(message)
        return await message.answer("Perintah tidak di temukan, Perlu bantuan ? /help",
                                    reply_markup=types.ReplyKeyboardRemove())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)