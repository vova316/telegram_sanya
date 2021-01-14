import asyncio
from aiogram import Bot, Dispatcher , executor

bot = Bot('1095886841:AAEAusYeBylFFAeXISpC41R3MWObUbDOcbA', parse_mode="HTML")
dp = Dispatcher(bot)

if __name__ == '__main__':
	from npd import dp
	from npd import scheduled
	dp.loop.create_task(scheduled(300))
	executor.start_polling(dp)
