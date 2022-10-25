from dataclasses import dataclass
from typing import List
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton


def create_reply_buttons_by(name_for_buttons: List, message_to_input_field: str = None) -> ReplyKeyboardMarkup:
    buttons: List[List["KeyboardButton"]] = [[]]

    for name_bt in name_for_buttons:
        buttons.append(
            [KeyboardButton(text=name_bt)]
        )

    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder=message_to_input_field
    )

    return keyboard


def create_inline_buttons_by(name_for_buttons: List) -> InlineKeyboardMarkup:
    # TODO: Сделать рендеринг кнопок в сообщении.
    ...




