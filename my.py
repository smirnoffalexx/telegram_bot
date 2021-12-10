import telebot
import datetime
import julian
import config

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Привет, Суетолог! Я - Альфа-версия Бота Макара. Для того, чтобы узнать работает ли сегодня Макар - напиши /today, чтобы узнать сегодняшний день по Юлианскому календарю - напиши /julian. В дальнейшем интерфейс будет обновляться и можно будет вводить любую дату. А пока что наводи суету!")

@bot.message_handler(commands=['today'])
def is_workday(message):
	base_date = datetime.date(2021, 12, 8) # Makar was on job since 9 a.m.
	day = datetime.date.today()
	delta = (day - base_date).days
	
	if delta % 4 == 0:
		bot.reply_to(message, "Вагнер сегодня работает!")
	elif delta % 4 == 1:
		bot.reply_to(message, "Вагнер сегодня работает!")
	elif delta % 4 == 2:
		bot.reply_to(message, "Вагнер сегодня Не работает, идем в кофейню!")
	else:
		bot.reply_to(message, "Вагнер сегодня Не работает, идем в кофейню!")

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
