# -*- coding: utf-8 -*-
import telebot
import sqlite3

from telebot import types
telebot.apihelper.proxy = {'https': 'socks5h://127.0.0.1:9150'}
bot = telebot.TeleBot('861716063:AAFKeX0xB3eNRsqxu8TMPqrQFCAr0fXtkjE')

name = ''
surname = ''
age = 0
uid = 0
club = "Real Madrid"
@bot.message_handler(content_types=['text'])
def start(message):
    keyboard = types.InlineKeyboardMarkup()
    key_reg = types.InlineKeyboardButton(text='/reg', callback_data='g')
    keyboard.add(key_reg)
    key_club = types.InlineKeyboardButton(text='/club', callback_data='f')
    keyboard.add(key_club)
    key_online = types.InlineKeyboardButton(text='/online', callback_data='h')
    keyboard.add(key_online)
    bot.send_message(message.from_user.id,text = "I have these options", reply_markup = keyboard);
    if message.text == "Привет" or message.text  == "Hello":
        bot.send_message(message.from_user.id, "Привет :)")
    elif message.text == '/reg':
        bot.send_message(message.from_user.id, "Как вас зовут?")
        bot.register_next_step_handler(message, get_name)
    elif message.text == '/club':
        with sqlite3.connect("clubs.db") as conn:
            cursor = conn.cursor()
            clubid = int(*cursor.execute('SELECT favourite_club_id FROM user WHERE user_id = ?', [message.from_user.id]).fetchone())
            url = cursor.execute('SELECT club_url FROM club WHERE club_id = ?', [clubid]).fetchone()[0]
            bot.send_message(message.from_user.id, url)
    elif message.text == '/online':
        bot.send_message(message.from_user.id, 'https://livesport.ws/football')
    else:
        bot.send_message(message.from_user.id, 'Напишите /reg')

def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Какая у вас фамилия?')
    bot.register_next_step_handler(message, get_surname)

def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Какой ваш любимый клуб?')
    keyboard = types.InlineKeyboardMarkup()
    key_1 = types.InlineKeyboardButton(text='Real Madrid', callback_data='1')
    keyboard.add(key_1)
    key_2 = types.InlineKeyboardButton(text='Barcelona', callback_data='2')
    keyboard.add(key_2)
    key_3 = types.InlineKeyboardButton(text='Manchester City', callback_data='3')
    keyboard.add(key_3)
    key_4 = types.InlineKeyboardButton(text='Manchester United', callback_data='4')
    keyboard.add(key_4)
    key_5 = types.InlineKeyboardButton(text='Chelsea', callback_data='5')
    keyboard.add(key_5)
    key_6 = types.InlineKeyboardButton(text='Bayern', callback_data='6')
    keyboard.add(key_6)
    bot.send_message(message.from_user.id,text = "Write one of them", reply_markup = keyboard)
    bot.register_next_step_handler(message, get_club)
                         
def get_club(message):
    global club
    club = message.text
    bot.send_message(message.from_user.id, 'Сколько вам лет?')
    bot.register_next_step_handler(message, get_age)
    

def get_age(message):
    global age
    i = 0
    temp = 0
    while temp == 0:
        try:
            age = int(message.text)
            temp = age
            i = 1
            if (age < 5):
                bot.send_message(message.from_user.id, 'Маленький такой :)');
        except Exception:
            age = 0
            bot.send_message(message.from_user.id, 'Повторите еще раз, пожалуйста')

    global uid
    uid += 1
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    key_either = types.InlineKeyboardButton(text='Не знаю', callback_data='either')
    keyboard.add(key_either)
    question = 'Тебе '+str(age)+' лет, тебя зовут '+name+' '+surname+ ' и твой любимый клуб '+ club + '?';
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        try:
            with sqlite3.connect("clubs.db") as conn:
                cursor = conn.cursor()
                clubid = int(*cursor.execute('SELECT club_id FROM club WHERE club_nm = ?', [club]).fetchone())
                cursor.execute('''
                    INSERT
                    INTO user (user_id, user_nm, favourite_club_id, age)
                    VALUES(?, ?, ?, ?)
                    ''', [uid, ' '.join([name, surname]), clubid, age])
                conn.commit()
            bot.send_message(call.message.chat.id, 'okey :)')
        except Exception as e:
            bot.send_message(call.message.chat.id, 'exception: {}'.format(e))
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'lol :)')
    elif call.data == "either":
        bot.send_message(call.message.chat.id, 'try again :)')
bot.polling(none_stop=True, interval=0)

