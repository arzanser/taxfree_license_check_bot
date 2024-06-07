from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup

from bot.config import *
from bot.text import MESSAGES
from bot.utils.check_input_data import check_car_number
from bot.utils.display_mosreg_license_data import print_mosreg_license

router = Router()

class MosregLicenseState(StatesGroup):
    car_number = State()

@router.message(Command("mosreglicense"))
async def mosreglicense_cmd(msg: Message, state: FSMContext) -> None:
    await state.set_state(MosregLicenseState.car_number)
    await msg.answer(MESSAGES["GET_CAR_NUMBER"])

@router.message(MosregLicenseState.car_number)
async def get_license_data(msg: Message, state: FSMContext) -> None:
    await state.update_data(car_number=msg.text)
    user_data = await state.get_data()
    await state.clear()
    car_number = user_data["car_number"].upper()
    file_path = QR_FILE_PATH.format(msg.from_user.id)
    if check_car_number(car_number):
        await print_mosreg_license(msg, car_number, file_path)
    else:
        await msg.answer(MESSAGES["WRONG_CAR_NUMBER"])