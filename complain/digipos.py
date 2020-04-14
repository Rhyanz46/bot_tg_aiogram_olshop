from aiogram import types


async def digipos_complain_handler(message: types.Message, state, reset_proxy, default_proxy):
    print(dir(state))
    print(message.text)
    pass
