import re, logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import BotConfig
from database import cnx

from complain import Complain

logging.basicConfig(level=logging.INFO)

bot_cfg = BotConfig()
bot = Bot(token=bot_cfg.token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
regex_special_character = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

complain = Complain(dp)
# group_id = '-471742296' bakuldata
group_id = '-471742296'

import asyncio
loop = asyncio.get_event_loop()
loop.run_until_complete(complain.load())


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


class UserForm(StatesGroup):
    name = State()  # Will be represented in storage as 'Form:name'
    age = State()  # Will be represented in storage as 'Form:age'
    gender = State()  # Will be represented in storage as 'Form:gender'


user_form = UserForm()


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


async def default_proxy(proxy) -> None:
    proxy.setdefault('buy', False)
    proxy.setdefault('do_verify_buy', False)
    proxy.setdefault('proses_beli', False)
    proxy.setdefault('kategori', False)
    proxy.setdefault('harus_ada_kategori', False)
    proxy.setdefault('joined', False)
    proxy.setdefault('beli_banyak', [])