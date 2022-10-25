from dataclasses import dataclass
from aiogram.fsm.state import StatesGroup, State


@dataclass
class FilterUserStates(StatesGroup):
    UserEnterTypeSport = State()
    UserEnterDistrict = State()
    UserEnterStatus = State()
    ReturnToStart = State()