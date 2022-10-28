from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards import render_buttons, street_sports_buttons, menus_buttons
from aiogram.filters.state import StateFilter
from api import sport_street_points as ssp
from handlers.street_sport import global_var as gv
from main import StartStates


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
    await message.answer("Подтверждаете?", reply_markup=render_buttons.create_reply_buttons_by(name_for_buttons=["✅  Да  ✅", "❌ Нет ❌"]))
    await state.set_state(FilterUserStates.Confirm)


@StreetSportRouter.message(StateFilter(FilterUserStates.Confirm))
async def show_results(message: Message, state: FSMContext):
    if message.text == "✅  Да  ✅":
        await message.answer("Выполняю поиск")
        await message.answer("Результаты")
        data = await state.get_data()
        Street = ssp.Street()
        gv.page += 1
        response = Street.get_part_data_by(activity=data["type_sport"], district=data["district"], page=gv.page)
        name_confirm_button = ["✅  Да  ✅", "❌  Нет  ❌"]
        for i in range(10):
            try:
                result = next(response)
                await message.answer(
                    f"Название: {result.name}\n"
                    f"Тип спорта {result.activity}\n"
                    f"Адрес: {result.address}\n"
                    f"Уточнение адреса: {result.addressy} \n"
                    f"Ближайшая станция метро: {result.metro}\n"
                    f"Контакты: {result.phone}\n" 
                    f"Время работы: {result.time}\n"
                )
            except StopIteration:
                await message.answer("Это все результаты по вашему запросу")
                name_confirm_button = ["Вернуться в меню", "Найти еще спортивные точки"]
                break

        await message.answer("Продолжить поиск?", reply_markup=render_buttons.create_reply_buttons_by(name_for_buttons=name_confirm_button))
        await state.set_state(FilterUserStates.Confirm)

    if message.text in ["❌  Нет  ❌", "Найти еще спортивные точки"]:
        gv.page = 0
        await message.answer("Выберите район", reply_markup=render_buttons.create_reply_buttons_by(street_sports_buttons.ButtonNames.district))
        await state.set_state(FilterUserStates.UserEnterDistrict)

    if message.text == "Вернуться в меню":
        gv.page = 0
        await message.answer("Выбрать поиск", reply_markup=render_buttons.create_reply_buttons_by(menus_buttons.menu_names))
        await state.set_state(StartStates.UserChooseSearch)





