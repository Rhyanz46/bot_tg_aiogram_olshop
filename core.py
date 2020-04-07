import re, logging
from aiogram import Bot, Dispatcher
from database import cnx
from config import BotConfig

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot_cfg = BotConfig()
bot = Bot(token=bot_cfg.token)
dp = Dispatcher(bot)
regex_special_character = re.compile('[@_!#$%^&*()<>?/\|}{~:]')


async def is_registered(id_user: int) -> bool:
    cursor = cnx.cursor(buffered=True)
    cursor.execute(f"SELECT telegram_id FROM user where telegram_id={id_user}")
    if cursor.fetchone():
        return True
    return False
