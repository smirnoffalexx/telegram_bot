import telebot
import datetime
import julian
from dotenv import load_dotenv
import os
import threading
import time
import json

load_dotenv()
api_token = os.getenv("API_TOKEN")
group_chat_id = os.getenv("CHAT_ID")
words = json.loads(os.getenv("WORDS"))
birthdays = json.loads(os.getenv("BIRTHDAYS"))
celebration_picture = os.getenv("PICTURE_URL")
celebration_gif = os.getenv("GIF_URL")
poll_command1 = json.loads(os.getenv("POLL_COMMAND1"))
poll_command2 = json.loads(os.getenv("POLL_COMMAND2"))

switchers = {}

def store_switcher(my_key, my_value):
	switchers[my_key] = dict(value=my_value)
  
def get_switcher(my_key):
 	return switchers[my_key].get('value')

def congratulation(bot):
	while True:
		try:
			current_time = datetime.datetime.now()
			if (current_time.hour == 10) and (current_time.minute == 0):
				date = current_time.date()
				for key in birthdays.keys():
					birthday = datetime.datetime.strptime(birthdays[key], '%Y-%m-%d').date()
					if (date.day == birthday.day) and (date.month == birthday.month):
						bot.send_message(group_chat_id, "{0}, Поздравляю с Днем Рождения!!!".format(key))
						bot.send_photo(group_chat_id, celebration_picture)
						bot.send_document(group_chat_id, celebration_gif)
						# time.sleep(60)
			if current_time.hour == 0 and current_time.minute == 0 and current_time.day == 1 and current_time.month == 1:
				bot.send_message(
					group_chat_id, 
					"Поздравляю всех работяг с Новым годом!!! Счастья, здоровья, успехов во всех начинаниях!"
				)
				bot.send_document(group_chat_id, celebration_gif)
		except Exception:
			print("Exception raised")
			pass
		except KeyboardInterrupt:
			print("KeyboardInterrupt raised")
			break
		time.sleep(60)

bot = telebot.TeleBot(api_token)

threading.Thread(target=congratulation, args=(bot,)).start()
    
@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Привет, Суетолог! Я - Бот Макара.\n Для того, чтобы узнать работает ли сегодня Макар - напиши /today.\n\
		Чтобы узнать работает ли Макар в рандомный день - введи /anydate, а затем дату в формате yyyy-mm-dd \
		(например, 2021-12-25).\n Чтобы узнать сегодняшний день по Юлианскому календарю - напиши /julian.\n\
		Дерзай и наводи суету!\n Чтобы включить режим беседы у бота - введи команду /switchon, чтобы отключить - /switchoff.\n\
		Также бот умеет поздравлять с ДР.")
	store_switcher(message.chat.id, True)
	print(message.chat.id) # helper for detecting chat id

@bot.message_handler(commands=['today'])
def today_is_workday(message):
	date = datetime.datetime.now().date()
	count_date(message, date)

@bot.message_handler(commands=['anydate'])
def any_date_is_workday(message):
	bot.send_message(message.chat.id, "Введи дату в формате yyyy-mm-dd, чтобы узнать работает ли Макар в этот день")
	bot.register_next_step_handler(message, anydate_parser)

def anydate_parser(message):
	try:
		any_date = datetime.datetime.strptime(message.text, '%Y-%m-%d').date()
		count_date(message, any_date)
	except ValueError:
		bot.reply_to(message, "Неверный формат. Нужна дата в формате yyyy-mm-dd. Повтори попытку, начиная с команды /anydate")

def count_date(message, any_date):
	# base_date = datetime.date(2021, 12, 8) # previous date
	base_date = datetime.date(2022, 6, 24) # Makar was on job since 9 a.m.
	delta = (any_date - base_date).days
	today = datetime.date.today()

	if (any_date - today).days >= 0:
		if delta % 4 == 0:
			bot.reply_to(message, "Макар работает! Он на работе с 9 утра до 9 вечера.")
		elif delta % 4 == 1:
			bot.reply_to(message, "Макар работает в ночь! Он на работе с 9 вечера, поэтому можно почилить до 7 вечера.")
		elif delta % 4 == 2:
			bot.reply_to(message, "Макар Не работает! Он приходит с работы в 10 утра. Можно идти в кофейню!")
		else:
			bot.reply_to(message, "Макар Не работает, можно идти в кофейню! У него полный выходной.")
	else:
		bot.reply_to(message, "Ты запросил день из прошлого. Повтори попытку, начиная с команды /anydate")

@bot.message_handler(commands=['julian'])
def julian_day(message):
	# now = datetime.datetime.now()
	date = datetime.date.today()
	day = date.day
	month = date.month
	year = date.year
	hour = 12
	minute = 0
	second = 0
	ms = 0
	date_full = datetime.datetime(year, month, day, hour, minute, second, ms)
	jd = int(julian.to_jd(date_full))
	bot.reply_to(message, "Сегодня %s день по Юлианскому календарю"%jd)

@bot.message_handler(commands=['switchon'])
def speaking_regime_on(message):
	store_switcher(message.chat.id, True)
	bot.reply_to(message, "Режим болтовни включен!")
	
@bot.message_handler(commands=['switchoff'])
def speaking_regime_off(message):
	store_switcher(message.chat.id, False)
	bot.reply_to(message, "Режим болтовни выключен!")

@bot.message_handler(commands=[poll_command1["command"]])
def send_poll_on_request1(message):
	bot.send_poll(
		message.chat.id, 
		poll_command1["question"], 
		options=[poll_command1["answer1"], poll_command1["answer2"], poll_command1["answer3"], poll_command1["answer4"]],
		is_anonymous="false"
	)

@bot.message_handler(commands=[poll_command2["command"]])
def send_poll_on_request2(message):
	bot.send_poll(
		message.chat.id, 
		poll_command2["question"], 
		options=[poll_command2["answer1"], poll_command2["answer2"], poll_command2["answer3"], poll_command2["answer4"]],
		is_anonymous="false"
	)

@bot.message_handler(func=lambda m: True)
def catch_phrase(message):
	try:
		switcher = get_switcher(message.chat.id)
		
		if switcher:
			for key in words.keys():
				if message.text.find(key) >= 0: # search(key, message.text): 
					bot.reply_to(message, words[key])
	except KeyError:
		store_switcher(message.chat.id, True)
		
bot.infinity_polling()
