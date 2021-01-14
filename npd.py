from main import bot, dp
from aiogram.types import Message
from nkey import menu, sub_menu
from aiogram.dispatcher.filters import Command, Text
import sqlite3
import pyowm
import requests
from bs4 import BeautifulSoup as bs
import asyncio

owm = pyowm.OWM('d856015103ff24d29128b3bb243278bc')

db = sqlite3.connect('SanyaBot.db') #настройки
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users(
	id TEXT,
	city TEXT
	)""")
db.commit()

sql.execute("""CREATE TABLE IF NOT EXISTS politic(
	id TEXT
	)""")
db.commit()

sql.execute("""CREATE TABLE IF NOT EXISTS games(
	id TEXT
	)""")
db.commit()

sql.execute("""CREATE TABLE IF NOT EXISTS space(
	id TEXT
	)""")
db.commit()

sql.execute("""CREATE TABLE IF NOT EXISTS datasubs(
	bdpol TEXT,
	bdgame TEXT,
	bdcos TEXT
	)""")
db.commit()

def citys(my_id, my_city):
	sql.execute(f"INSERT INTO users VALUES (?, ?)", (my_id, my_city))
	db.commit()

def new_sub(category, my_id):
	sql.execute(f"INSERT INTO {category} VALUES (?)", (my_id,))
	db.commit()

def delete_sub(category, my_id):
	sql.execute(f"DELETE FROM {category} WHERE id = '{my_id}'")
	db.commit()

#sql.execute("INSERT INTO datasubs VALUES (?, ?, ?)", ('', '', ''))
#db.commit()

URLpol = 'https://ria.ru/politics/'
URLgame = 'https://stopgame.ru/news'
URLcos = 'https://novosti-kosmonavtiki.ru/news/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}

def doing(table, status):
	sql.execute(f"UPDATE users SET " + table + "= " + status) # изменение данных
	db.commit()	

@dp.message_handler(Command('start'))
async def welcome(message: Message):
	global my_id
	my_id = message.from_user["id"]
	await bot.send_message(chat_id=message.from_user.id, text=f'Приветствую тебя, {message.from_user["first_name"]}, меня зовут Саня и я умею рассылать новости 😄', reply_markup=menu)

@dp.message_handler(Text('Помощь 🛠'))
async def help(message: Message):
	helper = "•Для перезапуска бота - /start" + "\n"
	helper += "•Для вызова списка команд - /help" + "\n"
	helper += "•Для нажатия на кнопку - нажмите на кнопку" + "\n"
	helper += "•Для того что бы узнать погоду нажмите на кнопку 'Погода'" + "\n"
	helper += "•Для того что бы подписаться/отписаться на политику - отправьте /politic" + "\n"
	helper += "•Для того что бы подписаться/отписаться на игры - отправьте /games" + "\n"
	helper += "•Для того что бы подписаться/отписаться на космос - отправьте /space" + "\n"
	helper += "•Что бы изменить ваш город введите: upd [ваш город]" + "\n\n"
	helper += "Список обновлений: " + "\n"
	helper += "•Бот был доведен до релизной версии" + "\n"
	helper += "SanyaBot v: 2.0.0"
	await bot.send_message(chat_id=message.from_user.id, text=helper)

@dp.message_handler(Text('Подписки ✉️'))
async def settings(message: Message):
	await bot.send_message(chat_id=message.from_user.id, text="Подписки:", reply_markup=sub_menu)


@dp.message_handler(Text('Политика 🧾'))
async def politic(message: Message):
	my_id = str(message.from_user["id"])
	ident = []
	subscribers = sql.execute("SELECT id FROM politic").fetchall()
	for s in subscribers:
		s = str(s)
		s = s[2:-3]
		ident.append(s)
	
	if my_id in ident:
		delete_sub("politic", my_id)
		await bot.send_message(chat_id=message.from_user.id, text="Ваша подписка отключена")
	else:
		new_sub("politic", my_id)
		await bot.send_message(chat_id=message.from_user.id, text="Ваша подписка подключена")
		
@dp.message_handler(Text('Игры 🎮'))
async def games(message: Message):
	my_id = str(message.from_user["id"])
	ident = []
	subscribers = sql.execute("SELECT id FROM games").fetchall()
	for s in subscribers:
		s = str(s)
		s = s[2:-3]
		ident.append(s)
	if my_id in ident:
		delete_sub("games", my_id)
		await bot.send_message(chat_id=message.from_user.id, text="Ваша подписка отключена")
	else:
		new_sub("games", my_id)
		await bot.send_message(chat_id=message.from_user.id, text="Ваша подписка подключена")

@dp.message_handler(Text('Космос 🚀'))
async def space(message: Message):
	my_id = str(message.from_user["id"])
	ident = []
	subscribers = sql.execute("SELECT id FROM space").fetchall()
	for s in subscribers:
		s = str(s)
		s = s[2:-3]
		ident.append(s)
	if my_id in ident:
		delete_sub("space", my_id)
		await bot.send_message(chat_id=message.from_user.id, text="Ваша подписка отключена")
	else:
		new_sub("space", my_id)
		await bot.send_message(chat_id=message.from_user.id, text="Ваша подписка подключена")

@dp.message_handler(Text('⬅️ Назад'))
async def exit(message: Message):
	await bot.send_message(chat_id=message.from_user.id, text="Меню:", reply_markup=menu)


@dp.message_handler(Text('Погода 🌤'))
async def weather(message: Message):
	my_id = message.from_user["id"]
	sql.execute(f"SELECT city FROM users WHERE id = '{my_id}'")
	if sql.fetchone() is None:
		place = 'Ваш город не зарегистрирован.'
	else:
		for val in sql.execute(f"SELECT city FROM users WHERE id = '{my_id}'"):
			place = val[0]
			mgr = owm.weather_manager()
			observation = mgr.weather_at_place(place)
			w = observation.weather
			temp = w.temperature('celsius')["temp"]
			wind = w.wind()["speed"]
			hum = w.humidity

			st = w.status

			if st == 'Clear':
				st = 'Ясно'
			elif st == 'Clouds':
				st = 'Облочно'
			elif st == 'Snow':
				st = 'Снежно'

			ans = "В городе сейчас: " + st + "\n" 
			ans += "Температура: " + str(temp) + "°C" + "\n"  
			ans += "Скорость ветра: " + str(wind) + "м/с" + "\n" 
			ans += "Влажность: " + str(hum) + "%" "\n\n"

			if temp < 10:
				ans += "Стоит одеть куртку"
			elif temp < 20:
				ans += "На улице прохладно"
			else:
				ans += "Погода просто замечательная, одежда на ваш вкус"
		await message.answer(ans)

@dp.message_handler(Command('city'))
async def city(message: Message):
	my_id = message.from_user["id"]
	sql.execute(f"SELECT city FROM users WHERE id = '{my_id}'")
	if sql.fetchone() is None:
		place = 'Ваш город не зарегистрирован.'
	else:
		for val in sql.execute(f"SELECT city FROM users WHERE id = '{my_id}'"):
			place = val[0]
	await bot.send_message(chat_id=message.from_user.id, text=f'Твой город: {place}')

@dp.message_handler(text_contains='upd')
async def new(message: Message):
	my_city = message.text[4:]
	my_id = message.from_user["id"]
	citys(my_id, my_city)
	await bot.send_message(chat_id=message.from_user.id, text='Зарегистрировано!')

async def scheduled(wait_for):
	while True:
		await asyncio.sleep(wait_for)
		response = requests.get(URLgame, headers = HEADERS)
		soup = bs(response.content, 'html.parser')
		items = soup.findAll('div', class_ = 'caption caption-bold') 
		comps = []

		for item in items:
			comps.append({'title': item.find('a').get_text(strip = True),
				'link': item.find('a').get('href')})

			d = comps
			d = d[:-19]
		d = str(d)
		de = d[-18:-3]
		ugame = "https://stopgame.ru"
		de = ugame + de

		sql.execute("SELECT bdgame FROM datasubs")
		nde = sql.fetchone()
		nde = str(nde)
		nde = nde[2:-3]
		if de != nde:
			sql.execute(f"UPDATE datasubs SET bdgame = '{de}'") # изменение данных
			db.commit()
			subscribers = sql.execute("SELECT id FROM games").fetchall()
			for s in subscribers:
				s = str(s)
				s = s[2:-3]
				await bot.send_message(chat_id=s, text=de, disable_notification = True)

		response = requests.get(URLpol, headers = HEADERS)
		soup = bs(response.content, 'html.parser')
		items = soup.findAll('div', class_ = 'list-item')
		comps = []

		for item in items:
			comps.append({'link': item.find('a', class_ = 'list-item__title color-font-hover-only').get('href')})
			e = comps
			e = e[:-19]
		e = str(e)
		fed = e[11:-3]

		ndf = sql.execute("SELECT bdpol FROM datasubs").fetchone()
		ndf = str(ndf)
		ndf = ndf[2:-3]

		if fed != ndf:
			sql.execute(f"UPDATE datasubs SET bdpol = '{fed}'")
			 # изменение данных
			db.commit()
			subscribers = sql.execute("SELECT id FROM politic").fetchall()
			for s in subscribers:
				s = str(s)
				s = s[2:-3]
				await bot.send_message(chat_id=s, text=fed, disable_notification = True)

		response = requests.get(URLcos, headers = HEADERS)
		soup = bs(response.content, 'html.parser')
		items = soup.findAll('div', class_ = 'row news-item')
		comps = []

		for item in items:
			comps.append({'title': item.find('a', class_ = 'news-info__top-title').get_text(strip = True),
				'link': item.find('a', class_ = 'news-info__top-title').get('href')})
			f = comps
			f = f[:-19]
		f = str(f)
		dg = f[-15:-3]
		ucos = "https://novosti-kosmonavtiki.ru"
		dg = ucos + dg

		sql.execute("SELECT bdcos FROM datasubs")
		ndg = sql.fetchone()
		ndg = str(ndg)
		ndg = ndg[2:-3]

		if dg != ndg:
			sql.execute(f"UPDATE datasubs SET bdcos = '{dg}'") # изменение данных
			db.commit()
			subscribers = sql.execute("SELECT id FROM space").fetchall()
			for s in subscribers:
				s = str(s)
				s = s[2:-3]
				await bot.send_message(chat_id=s, text=dg, disable_notification = True)
