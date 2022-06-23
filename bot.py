import telebot
import datetime
import julian
import config
# from re import search
import threading # import Thread
import time

switchers = {}

group_chat_id = "-1001581543375" # 818106094

birthdays = {
	"Сережа": datetime.datetime(1999, 4, 9, hour=9), # "09.04",
	"Макар": datetime.datetime(1998, 5, 14, hour=9), # "14.05", 
	"Саша QA": datetime.datetime(1998, 6, 6, hour=9), # "06.06",
	"Саша Blockchain": datetime.datetime(1998, 6, 17, hour=9), # "17.06", 
	"Матвей": datetime.datetime(1998, 9, 19, hour=9) # "19.09",
}

words = {
	"Привет": "Дороу",
	"привет": "Дороу",
	"Суета": "Никакой суеты!!!",
	"суета": "Никакой суеты!!!",
	"Отмена": "Отмена суеты!!!",
	"отмена": "Отмена суеты!!!",
	"Картатека": "Сережа???",
	"картатека": "Сережа???",
	"Алло": "Пицца???",
	"алло": "Пицца???",
	"Пицц": "Погнали в алло",
	"пицц": "Погнали в алло",
	"Пиво": "Я с вами",
	"пиво": "Я с вами",
	"Кофе": "Я с вами за кофе!",
	"кофе": "Я с вами за кофе!",
	"Хашбраун": "Без Сережи не пойду за хашбрауном!",
	"хашбраун": "Без Сережи не пойду за хашбрауном!",
	"Дима": "Опять тачки в инсте?",
	"дима": "Опять тачки в инсте?",
	"tiktok.com": "Опять тиктоки..."
}

def store_switcher(my_key, my_value):
	switchers[my_key] = dict(value=my_value)
  
def get_switcher(my_key):
 	return switchers[my_key].get('value')

def congratulation(bot):
	i = 0;
	while True:
		try:
			i = i + 1
			print(i)
			current_time = datetime.datetime.now()
			if (current_time.hour == 10) and (current_time.minute == 0):
				date = current_time.date()
				for key in birthdays.keys():
					if (date.day == birthdays[key].date().day) and (date.month == birthdays[key].date().month):
						bot.send_message(group_chat_id, "{0}, Поздравляю с Днем Рождения!!!".format(key))
						picture = open("Gosling_for_DR.jpg","rb")
						bot.send_photo(group_chat_id, picture)
						f = open("for_dr.mp4","rb")
						bot.send_document(group_chat_id, f)
						# time.sleep(60)
		except Exception:
			pass
		except KeyboardInterrupt:
			print("KeyboardInterrupt raised")
			break
		time.sleep(60)

bot = telebot.TeleBot(config.token)

threading.Thread(target=congratulation, args=(bot,)).start()
    
@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Привет, Суетолог! Я - Бот Макара.\n Для того, чтобы узнать работает ли сегодня Макар - напиши /today.\n\
		Чтобы узнать работает ли Макар в рандомный день - введи /anydate, а затем дату в формате yyyy-mm-dd\
		(например, 2021-12-25).\n Чтобы узнать сегодняшний день по Юлианскому календарю - напиши /julian.\n Дерзай и наводи суету!\n Чтобы включить режим беседы у бота - введи команду /switchon, чтобы отключить - /switchoff. Также бот умеет поздравлять с ДР.")
	store_switcher(message.chat.id, True)
	print(message.chat.id) # remove

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
	base_date = datetime.date(2021, 6, 24) # Makar was on job since 9 a.m.
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

@bot.message_handler(func=lambda m: True)
def catch_phrase(message):
	try:
		switcher = get_switcher(message.chat.id)
		
		if switcher:
			for key in words.keys():
				if message.text.find(key) >= 0: # search(key, message.text): 
					bot.reply_to(message, words[key])
				# else:
				#	bot.reply_to(message, "Тут нет ключевых слов")
	except KeyError:
		store_switcher(message.chat.id, True)
		
bot.infinity_polling()
		
# schedule.every().day.at("01:36").do(congratulation)

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
