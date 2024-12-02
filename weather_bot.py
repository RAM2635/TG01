import logging
import os
import requests
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from dotenv import load_dotenv

# Загрузка переменных из .env файла
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Функция для получения прогноза погоды
def get_weather(city_name: str) -> str:
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": WEATHER_API_KEY,
        "units": "metric",
        "lang": "ru"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        city = data["name"]
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]

        return f"Погода в городе {city}:\nТемпература: {temp}°C\nОписание: {description.capitalize()}"
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при запросе к API: {e}")
        return "Не удалось получить прогноз. Проверьте название города."

# Хендлер команды /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Привет! Отправьте название города, чтобы узнать погоду.")

# Хендлер текстовых сообщений (город)
@dp.message(F.text)
async def send_weather(message: Message):
    city_name = message.text
    weather_info = get_weather(city_name)
    await message.answer(weather_info)

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
