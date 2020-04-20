import re, logging, asyncio
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import BotConfig
from database import cnx

from complain import Complain

logging.basicConfig(level=logging.INFO)


class UserForm(StatesGroup):
    name = State()  # Will be represented in storage as 'Form:name'
    age = State()  # Will be represented in storage as 'Form:age'
    gender = State()  # Will be represented in storage as 'Form:gender'


user_form = UserForm()

bot_cfg = BotConfig()
bot = Bot(token=bot_cfg.token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
regex_special_character = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

# group_id = '-471742296' # bakuldata
group_id = '-452027376'  # sumber notif
# group_id = '-426065434'  # test


class User:
    def __init__(self):
        self.ok: bool = False
        self.telegram_id: int = 0
        self.telegram_username: str = ''
        self.kabupaten: str = ''
        self.kecamatan: str = ''
        self.nama_outlet: str = None
        self.nomor_mkios = None
        self.tgl_registrasi = None


class Order:
    def __init__(self):
        self.status: bool = False
        self.kode_barang: str = ''
        self.bot_message_id: int = 0
        self.telegram_id: int = 0
        self.qty: int = 0

    def get(self) -> dict:
        return {
            'status': self.status,
            'kode_barang': self.kode_barang,
            'bot_message_id': self.bot_message_id,
            'telegram_id': self.telegram_id,
            'qty': self.qty
        }


class ComplainDigiposData:
    def __init__(self, complain_id):
        self.complain_id = complain_id
        self.id = None
        self.status = None
        self.kabupaten = None
        self.telegram_id = None
        self.kecamatan = None
        self.id_outlet = None
        self.nama_outlet = None
        self.no_mkios = None
        self.no_pelanggan = None
        self.tgl_transaksi = None
        self.detail = None
        self.pay_method = None
        self.versi_apk_dipos = None
        self.channel_lain = None
        self.photo = None
        self.chat_id = None
        self.message_id = None
        self.handler_user_id = None
        self.created = None

    def new(self, data, telegram_id, complain_type=None, chat_id=None, message_id=None):
        photo = None
        if data['photo']:
            photo = data['photo']
            del data['photo']
        if photo:
            pass
        if complain_type == 'digipos':
            cursor = cnx.cursor(buffered=True)
            query_save_complain = ("INSERT INTO complain_digipos "
                                   "(complain_id, kabupaten, telegram_id, "
                                   "kecamatan, id_outlet, nama_outlet, no_mkios, no_pelanggan, "
                                   "tgl_transaksi, detail, pay_method, versi_apk_dipos, channel_lain, "
                                   "chat_id, message_id) "
                                   f'VALUES ("{self.complain_id}", %(kabupaten)s, {telegram_id}, %(kecamatan)s, '
                                   f'%(id_outlet)s, %(nama_outlet)s, %(no_mkios)s,  %(no_pelanggan)s, '
                                   f'%(tgl_transaksi)s, %(detail)s, %(pay_method)s, %(versi_apk_dipos)s, '
                                   f'%(channel_lain)s, "{chat_id}", "{message_id}")')
            cursor.execute(query_save_complain, data)
            cnx.commit()
        else:
            raise KeyError

    def set_status(self, status: str, admin_id: str):
        cursor = cnx.cursor(buffered=True)
        sql = f"UPDATE complain_digipos SET status = '{status}', handler_user_id = '{admin_id}' " \
              f"WHERE complain_id = '{self.complain_id}'"
        cursor.execute(sql)
        cnx.commit()

    def get(self):
        cursor = cnx.cursor(buffered=True)
        cursor.execute(f"SELECT * FROM complain_digipos where complain_id='{self.complain_id}'")
        complain_result = cursor.fetchone()
        if complain_result:
            self.id = complain_result[0]
            # self.complain_id = complain_result[1]
            self.status = complain_result[2]
            self.kabupaten = complain_result[3]
            self.telegram_id = complain_result[4]
            self.kecamatan = complain_result[5]
            self.id_outlet = complain_result[6]
            self.nama_outlet = complain_result[7]
            self.no_mkios = complain_result[8]
            self.no_pelanggan = complain_result[9]
            self.tgl_transaksi = complain_result[10]
            self.detail = complain_result[11]
            self.pay_method = complain_result[12]
            self.versi_apk_dipos = complain_result[13]
            self.channel_lain = complain_result[14]
            self.photo = complain_result[15]
            self.chat_id = complain_result[16]
            self.message_id = complain_result[17]
            self.handler_user_id = complain_result[18]
            self.created = complain_result[19]
            return self
        return self


class ComplainVoucherFisikData:
    def __init__(self, complain_id):
        self.id = None
        self.complain_id = complain_id
        self.telegram_id = None
        self.status = None
        self.kabupaten = None
        self.kecamatan = None
        self.nama_outlet = None
        self.id_digipos_outlet = None
        self.nomor_pelanggan = None
        self.serial_number = None
        self.tgl_inject_voucher = None
        self.paket = None
        self.masalah = None
        self.photo = None
        self.chat_id = None
        self.message_id = None
        self.handler_user_id = None
        self.created = None

    def new(self, data, telegram_id, complain_type=None, chat_id=None, message_id=None):
        photo = None
        if data['photo']:
            photo = data['photo']
            del data['photo']
        if photo:
            pass
        if complain_type == 'voucher_fisik':
            cursor = cnx.cursor(buffered=True)
            query_save_complain = ("INSERT INTO complain_voucher_fisik "
                                   "(complain_id, telegram_id, kabupaten, "
                                   "kecamatan, nama_outlet, id_digipos_outlet, nomor_pelanggan, "
                                   "serial_number, tgl_inject_voucher, paket, masalah, chat_id, "
                                   "message_id) "
                                   f'VALUES ("{self.complain_id}", {telegram_id}, %(kabupaten)s, %(kecamatan)s, '
                                   f'%(nama_outlet)s, %(id_digipos_outlet)s, %(nomor_pelanggan)s, '
                                   f'%(serial_number)s, %(tgl_inject_voucher)s, %(paket)s, %(masalah)s, '
                                   f'"{chat_id}", "{message_id}")')
            cursor.execute(query_save_complain, data)
            cnx.commit()
        else:
            raise KeyError

    def set_status(self, status: str, admin_id: str):
        cursor = cnx.cursor(buffered=True)
        sql = f"UPDATE complain_voucher_fisik SET status = '{status}', handler_user_id = '{admin_id}' " \
              f"WHERE complain_id = '{self.complain_id}'"
        cursor.execute(sql)
        cnx.commit()

    def get(self):
        cursor = cnx.cursor(buffered=True)
        cursor.execute(f"SELECT * FROM complain_voucher_fisik where complain_id='{self.complain_id}'")
        complain_result = cursor.fetchone()
        if complain_result:
            self.id = complain_result[0]
            # self.complain_id = complain_id
            self.telegram_id = complain_result[2]
            self.status = complain_result[3]
            self.kabupaten = complain_result[4]
            self.kecamatan = complain_result[5]
            self.nama_outlet = complain_result[6]
            self.id_digipos_outlet = complain_result[7]
            self.nomor_pelanggan = complain_result[8]
            self.serial_number = complain_result[9]
            self.tgl_inject_voucher = complain_result[10]
            self.paket = complain_result[11]
            self.masalah = complain_result[12]
            # self.photo = complain_result[13]
            self.chat_id = complain_result[14]
            self.message_id = complain_result[15]
            self.handler_user_id = complain_result[16]
            self.created = complain_result[17]
            return self
        return self


async def is_registered(id_user: int) -> User:
    cursor = cnx.cursor(buffered=True)
    cursor.execute(f"SELECT * FROM user where telegram_id={id_user}")
    user = cursor.fetchone()
    user_result = User()
    if user:
        user_result.ok = True
        user_result.telegram_id = user[0]
        user_result.telegram_username = user[1]
        user_result.kabupaten = user[2]
        user_result.kecamatan = user[3]
        user_result.nama_outlet = user[4]
        user_result.nomor_mkios = user[5]
        user_result.tgl_registrasi = user[6]
        return user_result
    return user_result


goods = {
    'buy_sp_reg': {
        'nama': 'SP Reg',
        'kategori': [
            {
                'kode': 'as_5k',
                'nama': 'AS 5K'
            },
            {
                'kode': 'simpati_10k',
                'nama': 'Simpati 10K'
            },
            {
                'kode': 'loop_5k',
                'nama': 'Loop 5K'
            }
        ]
    },
    'buy_sp_data': {
        'nama': 'SP Data',
        'kategori': [
            {
                'kode': '6/6.5gb',
                'nama': '6/6.5GB'
            },
            {
                'kode': '7.5/8gb',
                'nama': '7.5/8GB'
            },
            {
                'kode': '10gb',
                'nama': '10GB'
            }
        ]
    },
    'voucher_fisik': {
        'nama': 'Voucher Fisik',
        'kategori': [
            {
                'kode': '4gb',
                'nama': '4GB'
            },
            {
                'kode': '6.5gb',
                'nama': '6.5GB'
            },
            {
                'kode': '8gb',
                'nama': '8GB'
            }
        ]
    },
    'linkaja': {
        'nama': 'LinkAja',
    },
    'mkios': {
        'nama': 'Mkios',
    },
    'bulk': {
        'nama': 'Bulk',
    }
}


def semua_produk_yg_ada_kategorinya() -> list:
    hasil: list = []
    for item in goods:
        if goods[item].get('kategori'):
            hasil.append(item)
    return hasil


async def order_barang(order: Order):
    cursor = cnx.cursor(buffered=True)
    query = ("INSERT INTO orderan "
             "(telegram_id, kode_barang, qty) "
             "VALUES (%(telegram_id)s, %(kode_barang)s, %(qty)s)")
    cursor.execute(query, order.get())
    cnx.commit()
    # cursor.execute(f"SELECT * FROM user where telegram_id={id_user}")


async def reset_proxy(proxy, kecuali=None) -> None:
    for item in proxy:
        if kecuali and item in kecuali:
            continue
        proxy[item] = False


async def default_proxy(proxy, addtions=None) -> None:
    proxy.setdefault('buy', False)
    proxy.setdefault('do_verify_buy', False)
    proxy.setdefault('proses_beli', False)
    proxy.setdefault('kategori', False)
    proxy.setdefault('harus_ada_kategori', False)
    proxy.setdefault('joined', False)
    proxy.setdefault('complain_photo_require', False)
    proxy.setdefault('joined', False)
    proxy.setdefault('complain_chat_user_id_target', False)
    proxy.setdefault('beli_banyak', [])
    if addtions:
        for item in addtions:
            proxy.setdefault(f"{item}", addtions[item])


complain = Complain(dp, {
    'state': user_form,
    'methods': {
        'reset': reset_proxy,
        'default': default_proxy
    },
    'query': {
        'is_registered': is_registered
    }
})
loop = asyncio.get_event_loop()
loop.run_until_complete(complain.load())
