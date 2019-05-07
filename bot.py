import telebot;
from telebot import types
telebot.apihelper.proxy = {'https': 'socks5h://127.0.0.1:9150'}

bot = telebot.TeleBot('861716063:AAFfMdFpidnYeh8O_Evh-21dvn71e5gHhKM');

name = '';
surname = '';
age = 0;
club = "Real Madrid";
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет :)");
    elif message.text == '/reg':
        bot.send_message(message.from_user.id, "Как вас зовут?");
        bot.register_next_step_handler(message, get_name);
    else:
        bot.send_message(message.from_user.id, 'Напишите /reg');

def get_name(message):
    global name;
    name = message.text;
    bot.send_message(message.from_user.id, 'Какая у вас фамилия?');
    bot.register_next_step_handler(message, get_surname);

def get_surname(message):
    global surname;
    surname = message.text;
    bot.send_message(message.from_user.id, 'Какой ваш любимый клуб?');
    bot.register_next_step_handler(message, get_club);
                         
def get_club(message):
    global club;
    club = message.text;
    bot.send_message(message.from_user.id, 'Сколько вам лет?');
    bot.register_next_step_handler(message, get_age);
    

def get_age(message):
    global age;
    i = 0;
    temp = 0
    while temp == 0:
        try:
            age = int(message.text)
            temp = age
            i = 1;
            if (age < 18):
                bot.send_message(message.from_user.id, 'Маленький такой :)');
        except Exception:
            age = 0;
            bot.send_message(message.from_user.id, 'Повторите еще раз, пожалуйста');

    keyboard = types.InlineKeyboardMarkup();
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes');
    keyboard.add(key_yes);
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no');
    keyboard.add(key_no);
    key_either = types.InlineKeyboardButton(text='Не знаю', callback_data='either');
    keyboard.add(key_either);
    question = 'Тебе '+str(age)+' лет, тебя зовут '+name+' '+surname+ ' и твой любимый клуб '+ club + '?';
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, 'okey :)');
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'lol :)');
    elif call.data == "either":
        bot.send_message(call.message.chat.id, 'stupid :)');
bot.polling(none_stop=True, interval=0)
