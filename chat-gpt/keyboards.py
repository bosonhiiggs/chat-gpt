from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)
"""
Описаны клавиатуры:
    - Главного меню
    - Кнопки назад
"""

# Кнопки главного меню
main_menu_kb = [
    [
        KeyboardButton(text='Echo mode'),
        # KeyboardButton(text='GPT chat mode'),
     ],
    [
        KeyboardButton(text='GPT QA mode'),
        KeyboardButton(text='GPT Image mode'),
    ]
]

# Клавиатура на основе кнопок главного меню
keyboard_main_menu = ReplyKeyboardMarkup(
    keyboard=main_menu_kb,
    resize_keyboard=True,
    input_field_placeholder='Choice bot mode please',
)


# Кнопка назад
back_main_menu_bk = [[KeyboardButton(text='/back')]]

# Клавиатура на основе кнопки назад
keyboard_back_main_menu = ReplyKeyboardMarkup(
    keyboard=back_main_menu_bk,
    resize_keyboard=True,
)

