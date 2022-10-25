import asyncio
import config
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage

import handlers.street_sport.StreetSport
from handlers.street_sport.states import FilterUserStates
from keyboards import menus_buttons, street_sports_buttons
from keyboards import render_buttons, street_sports_buttons, menus_buttons

bot = Bot(token=config.Tele_Token)
dp = Dispatcher(storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

class StartStates(StatesGroup):
    Start = State()
    UserChooseSearch = State()


@dp.message(Command(commands=['start']))
async def start_bot(message: Message, state: FSMContext):
    await message.answer("Привет")
    await message.answer("Информация")
    await message.answer("Выбарть поиск", reply_markup=render_buttons.create_reply_buttons_by(menus_buttons.menu_names))
    await state.set_state(StartStates.UserChooseSearch)


@dp.message(StateFilter(StartStates.UserChooseSearch))
async def get_choose(message: Message, state: FSMContext):
    if message.text == "Найти дворовые спортивные точки":
        await message.answer("Переход на дворовые")
        await message.answer("Выберите район:", reply_markup=render_buttons.create_reply_buttons_by(street_sports_buttons.ButtonNames.district))
        await state.set_state(FilterUserStates.UserEnterDistrict)
    else:
        await message.answer("error")


async def main():
    logging.basicConfig(level=logging.INFO)

    dp.include_router(handlers.street_sport.StreetSport.StreetSportRouter)
    # dp.include_router(different_types.router)


    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())