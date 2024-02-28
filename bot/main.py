import asyncio
import logging
import configparser
import controller
from aiogram import Bot, Dispatcher


config_file = 'config.ini'
config = configparser.ConfigParser()
config.read(config_file)

TOKEN = config.get('bot', 'token')

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_routers(controller.router)

    logging.basicConfig(level=logging.INFO)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
