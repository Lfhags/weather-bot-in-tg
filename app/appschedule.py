from datetime import datetime, timedelta
import asyncio
from app.weather_utils import get_city_coordinates, get_weather, parse_weather_data, format_weather_message
from app.scheduler import scheduler

async def send_message_cron(bot, user_id, region):
    coordinates = await get_city_coordinates(region)
    if not coordinates:
        return
    
    lat, lon = coordinates
    weather_data = await get_weather(lat, lon)
    
    if not weather_data:
        print("Не вдалося отримати дані про погоду.")
        return
    
    parsed_data = parse_weather_data(weather_data)
    
    if parsed_data:
        current_weather = parsed_data[0]
        weather_message = format_weather_message(current_weather)
        
        await bot.send_message(
            user_id,
            f"🌤 Щоденний прогноз погоди для {region}:\n\n{weather_message}"
        )