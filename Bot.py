from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types
import requests


API_TOKEN = '5595724016:AAHoZm2V5ilAouNjCYQWavGFKzBcKA-3KRY'
weather_id='e173e2835b248384d08be500b4e16f26'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def log_writer(nm, ms, id):
    log = open('log.txt', 'a+', encoding='utf-8')
    log.write(f"{datetime.now()}\n{nm}\n{ms}\n{id}\n{'-'*40}\n")
    log.close


def weatherday(city):
    appid = "e173e2835b248384d08be500b4e16f26"
    res = requests.get("http://api.openweathermap.org/data/2.5/weather", params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
    data = res.json()
    try:
        return f'Прогноз погоды на день:\n\nГород: {city}\nПогодные условия: {data["weather"][0]["description"]}\nCкорость ветра: {data["wind"]["speed"]} м/с\nВидимость: {data["visibility"] / 100}%\nТемпература: {data["main"]["temp"]}\nМинимальная температура: {data["main"]["temp_min"]}\nМаксимальная температура: {data["main"]["temp_max"]}'
    except:
        return 0


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    log_writer(message.chat.full_name, message.text, message.chat.id)
    await message.reply("Привет, я могу рассказать о погоде.")


@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    log_writer(message.chat.full_name, message.text, message.chat.id)
    await message.reply("Для того чтобы получить погоду на день нужно написать /day <город>")


@dp.message_handler(commands=['day'])
async def main(message: types.Message):
    global weather_id
    log_writer(message.chat.full_name, message.text, message.chat.id)
    id = message.chat.id
    text = message.text.lower().split()
    print(message.text, message.chat.id)
    city = text[1]
    if weatherday(city) == 0:
        await message.reply("Я не смог найти твой город, пожалуйста проверь корректность города.")
    else:
        await message.reply(weatherday(city))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

