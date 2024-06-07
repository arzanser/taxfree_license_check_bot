import os

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.config import *
from bot.text import MESSAGES
from bot.utils.check_input_data import check_car_number
from bot.utils.display_mosru_license_data import print_mosru_license

router = Router()

class MosruLicenseState(StatesGroup):
    car_number = State()


@router.message(Command("mosrulicense"))
async def mosrulicense_cmd(msg: Message, state: FSMContext) -> None:
    await state.set_state(MosruLicenseState.car_number)
    await msg.answer(MESSAGES["GET_CAR_NUMBER"])


@router.message(MosruLicenseState.car_number)
async def get_license_data(msg: Message, state: FSMContext) -> None:
    await state.update_data(car_number=msg.text)
    user_data = await state.get_data()
    await state.clear()
    car_number = user_data["car_number"].upper()
    file_path = CAPTCHA_FILE_PATH.format(msg.from_user.id)
    if check_car_number(car_number):
        await print_mosru_license(msg, car_number, file_path) 
    else:
        await msg.answer(MESSAGES["WRONG_CAR_NUMBER"])



