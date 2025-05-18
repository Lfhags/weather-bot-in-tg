import requests
from config import WEATHER_API_KEY
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from app.appschedule import send_message_cron
from app.weather_utils import get_city_coordinates, get_weather, parse_weather_data, format_weather_message
from app.scheduler import scheduler

scheduler = AsyncIOScheduler()

async def get_city_coordinates(city_name: str):
    base_url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": f"{city_name},UA",  
        "limit": 1,
        "appid": WEATHER_API_KEY
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        if data and len(data) > 0:
            return data[0]["lat"], data[0]["lon"]
        return None
        
    except requests.RequestException as e:
        print(f"Помилка при отриманні координат: {e}")
        return None

async def get_weather(lat: float, lon: float):
    try:
        response = requests.get(
            "http://api.openweathermap.org/data/2.5/forecast",
            params={
                "lat": lat,
                "lon": lon,
                "appid": WEATHER_API_KEY,
                "units": "metric",
                "lang": "ua"
            }
        )
        return response.json()
    except:
        return None

def parse_weather_data(weather_data: dict) -> list:
    if not weather_data or 'list' not in weather_data:
        return []
    
    parsed_data = []
    for item in weather_data['list']:
        weather_info = {
            'datetime': datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S'),
            'temperature': round(item['main']['temp']),
            'feels_like': round(item['main']['feels_like']),
            'description': item['weather'][0]['description'],
            'humidity': item['main']['humidity'],
            'wind_speed': round(item['wind']['speed']),
            'clouds': item['clouds']['all']
        }
        parsed_data.append(weather_info)
    
    return parsed_data

def format_weather_message(weather_info: dict) -> str:
    return (
        f"🌡 Температура: {weather_info['temperature']}°C\n"
        f"🌤 Відчувається як: {weather_info['feels_like']}°C\n"
        f"📝 Опис: {weather_info['description']}\n"
        f"💧 Вологість: {weather_info['humidity']}%\n"
        f"💨 Вітер: {weather_info['wind_speed']} м/с\n"
        f"☁️ Хмарність: {weather_info['clouds']}%"
    )

async def schedule_weather_updates(bot: Bot, user_id: int, region: str, time: str):
    scheduler.add_job(
        send_message_cron,
        'cron',
        hour=int(time.split(':')[0]),
        minute=int(time.split(':')[1]),
        args=[bot, user_id, region],
        id=f'weather_{user_id}'
    )
    
    if not scheduler.running:
        scheduler.start()
    
    return True

def remove_weather_schedule(user_id: int):
    try:
        scheduler.remove_job(f'weather_{user_id}')
        return True
    except:
        return False