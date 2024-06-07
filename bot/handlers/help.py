from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from bot.text import MESSAGES

router = Router()

@router.message(Command("help"))
async def help_cmd(msg: Message) -> None:
    await msg.answer(MESSAGES["HELP_MESSAGE"])
