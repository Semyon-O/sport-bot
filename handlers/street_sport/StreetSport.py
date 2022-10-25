from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards import render_buttons, street_sports_buttons
from aiogram.filters.state import StateFilter


class FilterUserStates(StatesGroup):
    UserEnterTypeSport = State()
    UserEnterDistrict = State()
    UserEnterStatus = State()
    Confirm = State()


StreetSportRouter = Router()


@StreetSportRouter.message(StateFilter(FilterUserStates.UserEnterDistrict))
async def get_enter_district(message: Message, state: FSMContext):
    print(message)
    print(await state.get_data())
    await state.update_data(district=message.text)
    await message.answer("Выберите тип точки:", reply_markup=render_buttons.create_reply_buttons_by(street_sports_buttons.ButtonNames.type_sport))
    await state.set_state(FilterUserStates.UserEnterTypeSport)


@StreetSportRouter.message(StateFilter(FilterUserStates.UserEnterTypeSport))
async def get_enter_type_sport(message: Message, state: FSMContext):
    await state.update_data(type_sport=message.text)
    await message.answer("Выберите статус точки:", reply_markup=render_buttons.create_reply_buttons_by(street_sports_buttons.ButtonNames.status))
    await state.set_state(FilterUserStates.UserEnterStatus)


@StreetSportRouter.message(StateFilter(FilterUserStates.UserEnterStatus))
async def get_enter_status(message: Message, state: FSMContext):
    await state.update_data(status=message.text)
    result = await state.get_data()
    await message.answer(f"Вы выбрали: \n"
                         f"Район: <b>{result['district']}</b> \n"
                         f"Вид спорта: <b>{result['type_sport']}</b> \n"
                         f"Статус: <b>{result['status']}</b>",
                         parse_mode="HTML")
    await message.answer("Подтверждаете?", reply_markup=render_buttons.create_reply_buttons_by(name_for_buttons=["✅ Да ✅", "❌ Нет ❌"]))
    await state.set_state(FilterUserStates.Confirm)


@StreetSportRouter.message(StateFilter(FilterUserStates.Confirm))
async def confirm(message: Message, state: FSMContext):
    if message.text == "✅ Да ✅":
        await message.answer("Выполняю поиск")
    if message.text == "❌ Нет ❌":
        await message.answer("Возвращаю назад")
        await message.answer("Выберите район", reply_markup=render_buttons.create_reply_buttons_by(street_sports_buttons.ButtonNames.district))
        await state.set_state(FilterUserStates.UserEnterDistrict)


async def return_to_main_menu():
    ...


