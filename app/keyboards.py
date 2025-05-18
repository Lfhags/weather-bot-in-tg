from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, 
                           InlineKeyboardMarkup, InlineKeyboardButton,)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

contact_button = KeyboardButton(text="Поділитися контактом", request_contact=True)

keyboard = ReplyKeyboardMarkup(
    keyboard=[[contact_button]],  
    resize_keyboard=True,
    one_time_keyboard=True
)

regions = [
    "Вінниця", "Луцьк", "Дніпро", "Донецьк", "Житомир", "Ужгород", 
    "Запоріжжя", "Івано-Франківськ", "Київ", "Кропивницький", "Луганськ", "Львів", 
    "Миколаїв", "Одеса", "Полтава", "Рівне", "Суми", "Тернопіль", 
    "Харків", "Херсон", "Хмельницький", "Черкаси", "Чернівці", "Чернігів"
]

time = [
    "00:00", "01:00", "02:00", "03:00", "04:00", "05:00",
    "06:00", "07:00", "08:00", "09:00", "10:00", "11:00",
    "12:00", "13:00", "14:00", "15:00", "16:00", "17:00",
    "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"
]

async def inline_regions():
    builder = InlineKeyboardBuilder()
    for name in regions:
            builder.add(InlineKeyboardButton(text=name, callback_data=name))
    return builder.adjust(3).as_markup()

set_region = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Вибрати регіон")],
],
                    resize_keyboard=True,
                    input_field_placeholder='Виберіть пункт меню.')

settings_button = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Налаштування")]],
    resize_keyboard=True,
    input_field_placeholder='Виберіть пункт меню.')

settings_option = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Змінити регіон та час")],
        [KeyboardButton(text="Мій профіль")]
    ],
    resize_keyboard=True
)

def confirm_selection(region, time):
    message = f"Ви вибрали регіон: {region} та час: {time}."
    return settings_button, message








