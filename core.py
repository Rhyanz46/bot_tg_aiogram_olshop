import re, logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BotConfig
from database import cnx

logging.basicConfig(level=logging.INFO)

bot_cfg = BotConfig()
bot = Bot(token=bot_cfg.token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
regex_special_character = re.compile('[@_!#$%^&*()<>?/\|}{~:]')


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

group_id = '-471742296'

goods = {
    'buy_sp_reg': 'SP Reg',
    'buy_sp_data': 'SP Data',
    'voucher_fisik': 'Voucher Fisik',
    'linkaja': 'LinkAja',
    'mkios': 'Mkios',
    'bulk': 'Bulk'
}


async def order_barang(order: Order):
    cursor = cnx.cursor(buffered=True)
    query = ("INSERT INTO orderan "
             "(telegram_id, kode_barang, qty) "
             "VALUES (%(telegram_id)s, %(kode_barang)s, %(qty)s)")
    cursor.execute(query, order.get())
    cnx.commit()
    # cursor.execute(f"SELECT * FROM user where telegram_id={id_user}")
