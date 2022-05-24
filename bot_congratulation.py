import telebot
import datetime
import julian
import config
import time
# from re import search

bot = telebot.TeleBot(config.token)

group_chat_id = "-1001581543375" # 818106094

birthdays = {
	"Сережа": datetime.datetime(1999, 4, 9, hour=9), # "09.04",
	"Макар": datetime.datetime(1998, 5, 14, hour=9), # "14.05", 
	"Саша QA": datetime.datetime(1998, 6, 6, hour=9), # "06.06",
	"Саша Blockchain": datetime.datetime(1998, 6, 17, hour=9), # "17.06", 
	"Матвей": datetime.datetime(1998, 9, 19, hour=9) # "19.09",
}

def congratulation():
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
i = 0
while True:
	try:
		i = i + 1
		print(i)
		congratulation()
	except Exception:
		pass
	except KeyboardInterrupt:
		print("KeyboardInterrupt raised")
		break
	time.sleep(60)
	
	

	
