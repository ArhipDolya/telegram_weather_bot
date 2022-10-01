from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import datetime
import requests
import datetime


API_TOKEN = '5789445336:AAG-BuJv5rmvsKQFKQRGgmARxSYpKL6yJXU'
WEATHER_TOKEN = '1239028618ec658bdeec41e07a7fa57c'


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def get_weather(message: types.Message):
    smile_dict = {
        'Clear': 'Солнечно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождливо \U00002614',
        'Mist': 'Туман \U0001F32B',
        'Thunderstorm': 'Гроза \U000026A1',
        'Snow': 'Снежно \U0001F328'
    }

    try:
        req = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={WEATHER_TOKEN}&units=metric'
        )

        data = req.json()
        city = data['name']

        curr_temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        max_temp = data['main']['temp_max']
        min_temp = data['main']['temp_min']
        country = data['sys']['country']
        day_length = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(data['sys']['sunrise'])

        weather_desc = data['weather'][0]['main']
        if weather_desc in smile_dict:
            weather = smile_dict[weather_desc]
        else:
            weather = 'Не удалось узнать погоду города'

        await message.reply(f'Сегодняшняя дата и время: {datetime.datetime.now()}\n'
              f'Погода на улице: {weather}\n'
              f'Текущая температура: {curr_temp}\nНа сколько градусов температура чувствуется: {feels_like}\n'
              f'Максимальная температура: {max_temp}\n'
              f'Минимальная температура: {min_temp}\nСтрана: {country}\n'
              f'Продолжительность дня: {day_length}')

    except Exception as excep:
        await message.reply('Write a name of city correctly')
        await message.reply(f'You got an error - {excep}')


if __name__ == '__main__':
    executor.start_polling(dp)