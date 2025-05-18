from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, FSInputFile, ReplyKeyboardRemove
import app.keyboards as kb
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
import re
import app.database.requests as rq
from app.weather_service import get_city_coordinates, get_weather, schedule_weather_updates, remove_weather_schedule
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.appschedule import send_message_cron
from app.weather_service import format_weather_message


scheduler = AsyncIOScheduler(timezone="Europe/Kyiv")

router = Router()


class Reg(StatesGroup):
    number = State()


class Set_region(StatesGroup):
    region = State()


class Set_time(StatesGroup):
    time = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await rq.set_user(message.from_user.id)
    await state.set_state(Reg.number)
    await message.reply(f"{message.from_user.first_name}, вітаю! Для продовження користування ботом, необхідно пройти реєстрацію. Натисніть кнопку 'Поділитися контактом'.",
                         reply_markup=kb.keyboard)
    

@router.message(Reg.number, F.contact)
async def reg_number(message: Message, state: FSMContext):
    contact = message.contact
    if contact and contact.user_id == message.from_user.id:
        await state.update_data(number=contact.phone_number)
        data = await state.get_data()
        await message.answer(
            f"Дякуємо за реєстрацію.\n"
            f"Ім'я: {message.from_user.first_name}\n"
            f"Номер: {data['number']}", reply_markup=kb.set_region
        )
        await state.clear()
    else:
        await message.answer("Не вдалося отримати ваш контакт спробуйте ще раз")
    

@router.message(F.text == 'Вибрати регіон')
async def set_region(message: Message, state: FSMContext):
    await state.set_state(Set_region.region)
    await message.reply("Виберіть регіон нижче⬇️", reply_markup=await kb.inline_regions())


@router.callback_query(Set_region.region)
async def process_region_selection(callback: CallbackQuery, state: FSMContext):
    region = callback.data
    coordinates = await get_city_coordinates(region)
    if coordinates:
        lat, lon = coordinates
        await state.update_data(region=region, lat=lat, lon=lon)
        await rq.set_region(callback.from_user.id, region)
        await callback.message.edit_text(
            f"Вибрано регіон: {region}\n"
            f"Координати: {lat:.4f}, {lon:.4f}\n"
            f"Тепер введіть час у форматі HH:MM, щоб продовжити."
        )
        await state.set_state(Set_time.time)
    else:
        await callback.message.edit_text(
            f"Помилка: Не вдалося знайти координати для регіону {region}.\n"
            f"Будь ласка, спробуйте вибрати інший регіон."
        )
    
    await callback.answer()


@router.message(Set_time.time)
async def input_time(message: Message, state: FSMContext):
    time = message.text

    if not re.match(r"^([01]?\d|2[0-3]):[0-5]\d$", time):
        await message.answer("Невірний формат часу. Введіть час у форматі HH:MM (наприклад, 14:30).")
        return

    data = await state.get_data()
    region = data.get("region", "не вибрано")
    
    await rq.set_time(message.from_user.id, time)
    
    remove_weather_schedule(message.from_user.id)
    
    if await schedule_weather_updates(message.bot, message.from_user.id, region, time):
        await message.answer(
            f"✅ Налаштування збережено!\n"
            f"Вибрано регіон: {region}\n"
            f"Вибрано час: {time}\n"
            f"Ви будете отримувати погоду щодня о {time} для регіону {region}.\n"
            f"Для зміни регіону або часу, натисніть кнопку 'Налаштування'.",
            reply_markup=kb.settings_button
        )
    else:
        await message.answer(
            "❌ Помилка при налаштуванні розсилки погоди.\n"
            "Будь ласка, спробуйте ще раз.",
            reply_markup=kb.settings_button
        )
    
    await state.update_data(time=time) 
    await state.clear()


@router.message(F.text == 'Налаштування')
async def settings(message: Message):
    await message.answer("Виберіть пункт налаштувань:", reply_markup=kb.settings_option)


@router.message(F.text == 'Змінити регіон та час')
async def cahnge_region(message: Message, state: FSMContext):
    await state.set_state(Set_region.region)
    await message.answer("Виберіть регіон нижче⬇️", reply_markup=await kb.inline_regions())


@router.message(F.text == 'Змінити час')
async def change_time(message: Message, state: FSMContext):
    await message.answer("Введіть новий час у форматі HH:MM")
    await state.set_state(Set_time.time)


@router.message(F.text == 'Мій профіль')
async def my_profile(message: Message, state: FSMContext):
    data = await state.get_data()
    region = data.get("region", "не вибрано") 
    time = data.get("time", "не вибрано")  


    await message.answer(
        f"Ваш профіль:\n"
        f"Ваше ім'я: {message.from_user.first_name}\n"
        f"Ваш регіон: {region}\n"
        f"Ваш час: {time}",
        reply_markup=kb.settings_option
    )
