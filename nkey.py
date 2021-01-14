from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
	keyboard=[
	[
	KeyboardButton(text="Погода 🌤"),
	KeyboardButton(text="Помощь 🛠"),
	],
	[
	KeyboardButton(text="Подписки ✉️"),
	],
	],
	resize_keyboard=True
	)



sub_menu = ReplyKeyboardMarkup(
	keyboard=[
	[
	KeyboardButton(text="Политика 🧾"),
	KeyboardButton(text="Игры 🎮"),
	KeyboardButton(text="Космос 🚀"),
	],
	[
	KeyboardButton(text="⬅️ Назад"),
	],
	],
	resize_keyboard=True
	)
