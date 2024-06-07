import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import *
from bot.handlers import start, help, mosreglicense, mosrulicense


async def main() -> None:
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(
        start.router, 
        help.router, 
        mosreglicense.router, 
        mosrulicense.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)#, filename="log.log", filemode="w")
    asyncio.run(main())
