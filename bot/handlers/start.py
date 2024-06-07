from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from bot.text import MESSAGES

router = Router()

@router.message(Command("start"))
async def start_cmd(msg: Message) -> None:
    await msg.answer(MESSAGES["START_MESSAGE"])
