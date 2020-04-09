import re, logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database import cnx
from config import BotConfig

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot_cfg = BotConfig()
bot = Bot(token=bot_cfg.token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
regex_special_character = re.compile('[@_!#$%^&*()<>?/\|}{~:]')


async def is_registered(id_user: int) -> bool:
    cursor = cnx.cursor(buffered=True)
    cursor.execute(f"SELECT telegram_id FROM user where telegram_id={id_user}")
    if cursor.fetchone():
        # cnx.close()
        return True
    return False

goods = {
            'buy_sp_reg': 'SP Reg',
            'buy_sp_data': 'SP Data',
            'voucher_fisik': 'Voucher Fisik',
            'linkaja': 'LinkAja',
            'mkios': 'Mkios',
            'bulk': 'Bulk'
        }
