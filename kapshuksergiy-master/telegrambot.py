import telebot 
from telebot import types 
import app.const 
import sqlalchemy 
import app.alch_class
import datetime
import calendar
from flask import render_template


bot = telebot.TeleBot(app.const.API_TOKEN)

# markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 1 , one_time_keyboard = True)
# serch_ticket = types.KeyboardButton("Начать поиск")
# s_help = types.KeyboardButton("Доп. информация ")
# markup_menu.add(serch_ticket, s_help)

state = 0

station_dep = ''
station_arr = ''
id_wagos = 0
id_train = 0 
number_places = 0
typ_wagon = ''
dataa = 0

@bot.message_handler(commands=['start'])
def send_welcome(message):
	markup_menu_1 = types.InlineKeyboardMarkup()
	serch_ticket = types.InlineKeyboardButton('Начать поиск', callback_data = 'qwer')
	s_help = types.InlineKeyboardButton('Доп.информация', callback_data = 'wert')
	ver_bil = types.InlineKeyboardButton('Вернуть билет',url='http://127.0.0.1:5000/')
	check_ticket = types.InlineKeyboardButton('check_ticket',callback_data = 'check_ticket')
	# ghhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
	markup_menu_1.add(serch_ticket, s_help,ver_bil)
	markup_menu_1.add(check_ticket)
	bot.reply_to(message, "Привет) я бот по поиску билетов", reply_markup = markup_menu_1)


if len(set((app.alch_class.select_station_arrival()))) >= 3:
	dep_city = types.InlineKeyboardMarkup()
	a = list(set((app.alch_class.select_station_arrival())))
	dep_city1 = types.InlineKeyboardButton('{}'.format(a[0][0]), callback_data = '{}'.format(a[0][0]))
	dep_city2 = types.InlineKeyboardButton('{}'.format(a[1][0]), callback_data ='{}'.format(a[1][0]))

	dep_city.add(dep_city1, dep_city2)

def create_calendar():
	now = datetime.datetime.now()
	month_a = [1,3,5,7,8,10]
	month_b = [4,6,9,11]
	month_c = [2]
	month_d = [12]
	calendar_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 2, one_time_keyboard=True)
	mont = now.month
	dayy = now.day
	year = now.year
	flag = 1
	if mont in month_a:
		for i in range(29):
			if dayy != 32:
				dayy += 1	
			elif dayy == 32:
				dayy = 1
				mont += 1
			if flag == 1:
				md_1 = types.KeyboardButton('{}-{}-{}'.format(year,mont,dayy))
				flag = 2
			elif(flag == 2):
				md_2 = types.KeyboardButton('{}-{}-{}'.format(year,mont,dayy))
				calendar_menu.add(md_1,md_2) 
				flag = 1
	elif now.month in month_b:		
		for i in range(29):
			if dayy != 31:
				dayy += 1	
			elif dayy == 31:
				dayy = 1
				mont += 1
			if flag == 1:
				md_1 = types.KeyboardButton('{}-{}-{}'.format(year,mont,dayy))
				flag = 2
			elif(flag == 2):
				md_2 = types.KeyboardButton('{}-{}-{}'.format(year,mont,dayy))
				calendar_menu.add(md_1,md_2) 
				flag = 1
	elif now.month == month_c:
		for i in range(29):
			if dayy != 29:
				dayy += 1	
			elif dayy == 29:
				dayy = 1
				mont += 1
			if flag == 1:
				md_1 = types.KeyboardButton('{}-{}-{}'.format(year,mont,dayy))
				flag = 2
			elif(flag == 2):
				md_2 = types.KeyboardButton('{}-{}-{}'.format(year,mont,dayy))
				calendar_menu.add(md_1,md_2) 
				flag = 1
	elif now.month in month_d:		
		for i in range(30):
			if dayy != 32:
				dayy += 1	
			elif dayy == 32:
				dayy = 1
				mont = 1
				year += 1
			if flag == 1:
				md_1 = types.KeyboardButton('{}-{}-{}'.format(year,mont,dayy))
				flag = 2
			elif(flag == 2):
				md_2 = types.KeyboardButton('{}-{}-{}'.format(year,mont,dayy))
				calendar_menu.add(md_1,md_2) 
				flag = 1
	return calendar_menu
# def get_calendar(message):
#     now = datetime.datetime.now() #Текущая дата
#     chat_id = message.chat.id
#     date = (now.year,now.month)
#     current_shown_dates[chat_id] = date #Сохраним текущую дату в словарь
#     markup = calendar.create_calendar(now.year,now.month)
#     bot.send_message(message.chat.id, "Пожалйста, выберите дату", reply_markup=markup)

def ticket_to_ride(call):
	dat = app.alch_class.select_date_by_id_statio(id_train,station_dep,station_arr)

	bot.reply_to(call.message, "Ви замовили білет на потяг № {} {} - {},\nДата відправлення  {}  Дата прибуття {} \nТип Вагону '{}' Вагон № {} Місце № {} ".format(id_train,station_dep,station_arr,dat[0][0],dat[0][1],typ_wagon,id_wagos,number_places))


def keybord_id_train(data ,station_d,station_a):
	idd_train = types.InlineKeyboardMarkup()
	back = types.InlineKeyboardButton('BACK',callback_data = 'BACK_2')
	if app.alch_class.select_train_by_date(data, station_d,station_a) != []:
		for train in app.alch_class.select_train_by_date(data, station_d,station_a):
			key_train = types.InlineKeyboardButton("{}".format(train[0]), callback_data = '{}'.format(train[0]))
			idd_train.add(key_train)
	idd_train.add(back)
	return idd_train

def keybord_free_places(idd_train,id_wagon):
	free_pla = types.InlineKeyboardMarkup()
	pla = []
	flag = 1
	for pleces in app.alch_class.select_free_places(idd_train,id_wagon)[0]:
		if flag == 1: 
			pla_1 = types.InlineKeyboardButton('{}'.format(pleces), callback_data = '{}'.format(pleces))
			flag = 2
		elif flag == 2:
			pla_2 = types.InlineKeyboardButton('{}'.format(pleces), callback_data = '{}'.format(pleces))
			flag = 3 
		elif flag == 3:
			pla_3 = types.InlineKeyboardButton('{}'.format(pleces), callback_data = '{}'.format(pleces))
			flag = 1 
			free_pla.add(pla_1,pla_2,pla_3)
	if flag == 2 :
		free_pla.add(pla_1)
	elif flag == 3:
		free_pla.add(pla_1,pla_2)
	back = types.InlineKeyboardButton('Back',callback_data = 'BACK_4')
	free_pla.add(back)
	return free_pla

def keybord_w(idd_train, typ_wagon):
	keybord_wagons = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 2, one_time_keyboard=True)
	for wagon in app.alch_class.select_wagon_by_id_type(idd_train,typ_wagon):
		key_wagons = types.KeyboardButton('{}'.format(wagon[0]))
		keybord_wagons.add(key_wagons)
	key_back = types.KeyboardButton('BACK')
	keybord_wagons.add(key_back)
	return keybord_wagons

def keybord_type_wagon(idd_train):
	t_wagon = types.InlineKeyboardMarkup()
	pla = 0
	cup = 0
	keybo_back = types.InlineKeyboardButton('BACK',callback_data= 'BACK_3')
	for i in app.alch_class.select_wagon_places_by_id(idd_train):
		if i[1] == 'Плацкарт':
			pla += len(i[0])
		elif i[1] == 'Купе':
			cup += len(i[0])

	if pla != 0:
		keybo_pla = types.InlineKeyboardButton('Плацкарт - {}'.format(pla), callback_data = 'Плацкарт')
		t_wagon.add(keybo_pla)
	if cup != 0:
		keybo_cup = types.InlineKeyboardButton('Купе - {}'.format(cup), callback_data = 'Купе')
		t_wagon.add(keybo_cup)
	t_wagon.add(keybo_back)
	return t_wagon

def keyboard_but_arr(station):
	arrival_city = types.InlineKeyboardMarkup()
	flag = 1
	for ar_ct in app.alch_class.select_station_arrival():
		if (ar_ct[0] != station) and (flag == 1):
			ar_ct_1 = ar_ct[0]
			arriv_city1 = types.InlineKeyboardButton( ar_ct[0], callback_data = '{}'.format(ar_ct[0]))
			flag = 2
		if (ar_ct[0] != station) and (flag == 2) and (ar_ct[0] != ar_ct_1):
			arriv_city2 = types.InlineKeyboardButton( ar_ct[0], callback_data = '{}'.format(ar_ct[0]))
			flag = 0
	arrival_city.add(arriv_city1,arriv_city2)
	return arrival_city

# def date_picker(station_d,station_a):
	
# 	for i in [i[0] for i in alch_class.select_id_by_station(station_d,station_a)]


@bot.callback_query_handler(func=lambda call: call.data)
def incline (call):
	global state
	global station_dep
	global station_arr
	global id_train
	global typ_wagon
	global number_places
	if state == 1 and len(set(app.alch_class.select_station_arrival())) >= 3:
		state = 2
		# aarray1 = alch_class.select_station_deprt()
		# print(aarray1)
		station_dep = call.data
		# for station in alch_class.select_station_deprt():
		# 	if station[0] == call.data:
		
		arrival_city = types.InlineKeyboardMarkup()
		flag = 1
		for ar_ct in app.alch_class.select_station_arrival():
			if (ar_ct[0] != call.data) and (flag == 1):
				ar_ct_1 = ar_ct[0]
				arriv_city1 = types.InlineKeyboardButton( ar_ct[0], callback_data = '{}'.format(ar_ct[0]))
				flag = 2
			if (ar_ct[0] != call.data) and (flag == 2) and (ar_ct[0] != ar_ct_1):
				arriv_city2 = types.InlineKeyboardButton( ar_ct[0], callback_data = '{}'.format(ar_ct[0]))
				flag = 0

		arrival_city.add(arriv_city1,arriv_city2)
		# print(station_dep)
		# print('3')
		bot.reply_to(call.message,"Напишите станцию прибытия", reply_markup = arrival_city)
	elif(call.data == 'BACK_2'):
		state = 3 
		bot.reply_to(call.message, 'Выберите дату', reply_markup = create_calendar())
	elif(call.data == 'BACK_3'):
		st = ''
		new_data = datetime.datetime.strptime(dataa, "%Y-%m-%d")
		train_by_data = app.alch_class.select_train_by_date(new_data.date(),station_dep,station_arr)
		if train_by_data != []:
			for i in train_by_data:
				data = app.alch_class.select_date_by_id_statio(i[0],station_dep,station_arr)
				free_places = 0
				for j in app.alch_class.select_wagon_places_by_id(i[0]):
					free_places += len(j[0])
				st += "№{} . {} - {} . {} - {} свободніх мест {} \n".format(i[0], station_dep,station_arr,data[0][0],data[0][1],free_places)
		else: st = '------------------------'
		bot.reply_to(call.message, st , reply_markup = keybord_id_train(new_data.date(), station_dep,station_arr) )
		state = 4

	# elif(call.data == 'vern'):
	# 	return render_template('ticket.html')

	elif(call.data == 'BACK_4'):
		bot.reply_to(call.message,'Выберите номер вагона', reply_markup = keybord_w(id_train,typ_wagon))

	elif (call.data == 'qwer'):
		state = 1
		if len(set(app.alch_class.select_station_arrival())) >= 3:
			bot.reply_to (call.message, "Напишите город отправитель или выберите з доступных ",reply_markup = dep_city)
		else:
			bot.reply_to (call.message, "Напишите город отправитель ")


	elif (call.data == 'check_ticket'):
		st = ""
		if app.alch_class.select_users_ticket(str(call.message.from_user.id)) != []:
			for i in app.alch_class.select_users_ticket(str(call.message.from_user.id)):
				
				st += str(i)
		else:
			st = 'Вы ещё закакзывали билеты'

		bot.reply_to(call.message,st)

	elif(call.data == 'wert'):
		bot.reply_to(call.message," Бот по поисук билетов на територии Украины ")
		markup_menu_1 = types.InlineKeyboardMarkup()
		serch_ticket = types.InlineKeyboardButton('Начать поиск', callback_data = 'qwer')
		s_help = types.InlineKeyboardButton('Доп.информация', callback_data = 'wert')
		ver_bil = types.InlineKeyboardButton('Вернуть билет', callback_data = 'vern')
		check_ticket = types.InlineKeyboardButton('check_ticket',callback_data = 'check_ticket')
		# ghhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
		markup_menu_1.add(serch_ticket, s_help,ver_bil)
		markup_menu_1.add(check_ticket)
		bot.reply_to(call.message, "Привет) я бот по поиску билетов", reply_markup = markup_menu_1)
	elif( state == 2 ):
		state = 3 
		station_arr = call.data
		print(station_arr)
		print(station_dep)
		bot.reply_to(call.message, 'Выберите дату', reply_markup = create_calendar())
	elif( state == 4 ):
		id_train = call.data
		print(id_train)
		bot.reply_to(call.message, 'Выберите тип вагона ', reply_markup = keybord_type_wagon(id_train)) 
		state = 5	
	elif(call.data == 'Плацкарт' or call.data == 'Купе'):
		typ_wagon = call.data 
		print(typ_wagon)
		# print(id_train)
		bot.reply_to(call.message,'Выберите номер вагона', reply_markup = keybord_w(id_train,typ_wagon))
	elif (state == 5 ):
		number_places = call.data
		app.alch_class.ticket_purchase(id_train,id_wagos,int(number_places))
		dat = app.alch_class.select_date_by_id_statio(id_train,station_dep,station_arr)
		app.alch_class.add_users(call.message.from_user.id,id_train,id_wagos,station_dep,station_arr,dat[0][0],dat[0][1],typ_wagon,number_places)
		ticket_to_ride(call)

		

@bot.message_handler(content_types=['text'])
def ne_znay(message):
	global state
	global station_arr
	global station_dep
	global id_wagos
	global dataa
	# print(state)
	if (state == 1):
		deprt_station = [i[0] for i in app.alch_class.select_station_deprt()]
		# print(deprt_station)
		if message.text in deprt_station:
			station_dep = message.text
			state = 2

			if len(set(app.alch_class.select_station_arrival())) >= 3:
				bot.reply_to(message,"Напишите станцию прибытия", reply_markup = keyboard_but_arr(station_dep))
			else:
				# print('dfs')
				bot.reply_to(message,"Напишите станцию прибытия")
		else:
			if len(set(app.alch_class.select_station_arrival())) >= 3:
				bot.reply_to(message, " Неправильное название ", reply_markup = dep_city)
			else:
				bot.reply_to(message, " Неправильное название,поробуйте ещё раз")

	elif(state == 2):

		if message.text in [i[0] for i in app.alch_class.select_station_arrival()]:
			station_arr = message.text
			state = 3
			print(station_arr)
			print(station_dep)
			create_calendar()
			bot.reply_to(message, 'Выберите дату', reply_markup = create_calendar())
		else:
			# print('dsfdsfdsfdsfsdfds')
			# print(station_dep)
			# print(keyboard_but_arr(station_dep))
			if len(set(app.alch_class.select_station_arrival())) >= 3:
				# print('1')
				bot.reply_to(message,"Напишите станцию прибытия", reply_markup = keyboard_but_arr(station_dep))
			else:
				# print('2')
				bot.reply_to(message,"Напишите станцию прибытия")
	# else: 
	# 	incline('qwer')
	elif(state == 3):
		st = ''
		dataa = message.text
		new_data = datetime.datetime.strptime(dataa, "%Y-%m-%d")
		train_by_data = app.alch_class.select_train_by_date(new_data.date(),station_dep,station_arr)
		if train_by_data != []:
			for i in train_by_data:
				data = app.alch_class.select_date_by_id_statio(i[0],station_dep,station_arr)
				free_places = 0
				for j in app.alch_class.select_wagon_places_by_id(i[0]):
					free_places += len(j[0])
				st += "№{} . {} - {} . {} - {} свободніх мест {} \n".format(i[0], station_dep,station_arr,data[0][0],data[0][1],free_places)
		else: st = '------------------------'
		bot.reply_to(message, st , reply_markup = keybord_id_train(new_data.date(), station_dep,station_arr) )
		state = 4
	
	elif (state == 5):
		if message.text == 'BACK':
			bot.reply_to(message, 'Выберите тип вагона ', reply_markup = keybord_type_wagon(id_train)) 
			state = 5	
		else:
			id_wagos = message.text
			print(id_wagos)
			if typ_wagon == 'Плацкарт':
				bot.send_photo(message.chat.id, app.const.url_photo_pl)
			if typ_wagon == 'Купе':
				bot.send_photo(message.chat.id, app.const.url_photo_cu)	
			bot.reply_to(message,'Выберите номер места',reply_markup = keybord_free_places(id_train,message.text))
		

bot.polling()

