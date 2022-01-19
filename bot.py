import telebot
import datetime
import julian
import config

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Привет, Суетолог! Я - Бета-версия Бота Макара.\n Для того, чтобы узнать работает ли сегодня Макар - напиши /today.\n\
		Чтобы узнать работает ли Макар в рандомный день - введи /anydate, а затем дату в формате yyyy-mm-dd\
		(например, 2021-12-25).\n Чтобы узнать сегодняшний день по Юлианскому календарю - напиши /julian.\n Дерзай и наводи суету!")

@bot.message_handler(commands=['today'])
def today_is_workday(message):
	base_date = datetime.date(2021, 12, 8) # Makar was on job since 9 a.m.
	day = datetime.date.today()
	delta = (day - base_date).days
	
	if delta % 4 == 0:
		bot.reply_to(message, "Вагнер сегодня работает! Он на работе с 9 утра.")
	elif delta % 4 == 1:
		bot.reply_to(message, "Вагнер сегодня работает! Он на работе с 9 вечера, поэтому можно почилить до 7 вечера.")
	elif delta % 4 == 2:
		bot.reply_to(message, "Вагнер сегодня Не работает, идем в кофейню! Он приходит с работы в 10.30 утра.")
	else:
		bot.reply_to(message, "Вагнер сегодня Не работает, идем в кофейню! У него сегодня полный выходной.")

@bot.message_handler(commands=['anydate'])
def any_date_is_workday(message):
	bot.send_message(message.chat.id, "Введи дату в формате yyyy-mm-dd, чтобы узнать работает ли Макар в этот день")
	bot.register_next_step_handler(message, count_date)

def count_date(message):
	try:
		any_day = datetime.datetime.strptime(message.text, '%Y-%m-%d')
		base_date = datetime.datetime(2021, 12, 8, 0, 0) # Makar was on job since 9 a.m.
		delta = (any_day - base_date).days
		today = datetime.datetime.today()
		delta_today = (any_day - today).days

		if delta_today >= 0:
			if delta % 4 == 0:
				bot.reply_to(message, "Вагнер работает! Он на работе с 9 утра.")
			elif delta % 4 == 1:
				bot.reply_to(message, "Вагнер работает! Он на работе с 9 вечера, поэтому можно почилить до 7 вечера.")
			elif delta % 4 == 2:
				bot.reply_to(message, "Вагнер Не работает, можно идти в кофейню! Он приходит с работы в 10.30 утра.")
			else:
				bot.reply_to(message, "Вагнер Не работает, можно идти в кофейню! У него полный выходной.")
		else:
			bot.reply_to(message, "Ты запросил день из прошлого. Повтори попытку, начиная с команды /anydate")
	except ValueError:
		bot.reply_to(message, "Неверный формат. Нужна дата в формате yyyy-mm-dd. Повтори попытку, начиная с команды /anydate")

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
	
bot.infinity_polling()

# If I want to check date format without handling an exception:
# import re

# strings = ["8:30:00", "16:00:00", "845:00", "aa:bb:00"]

# for s in strings:
#     if re.match("\d{1,2}:\d{2}:\d{2}", s):  # Will return True if pattern matches s
#         print("match: {}".format(s))  # Take action on a matching pattern
#     else:
#         print("no match: {}".format(s))

# day = datetime.datetime.strptime('2014-01-01', '%Y-%m-%d').timetuple().tm_yday

#@bot.message_handler(func=lambda m: True)
#def echo_all(message):
#	bot.reply_to(message, message.text)
