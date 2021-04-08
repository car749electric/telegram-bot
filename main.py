import telebot
from telebot import types

from credentials import bot_id

bot = telebot.TeleBot(bot_id)

'''@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if "привет" in message.text:
        bot.send_message(message.from_user.id, "пока")
    else:
        bot.send_message(message.from_user.id, "я нахажусь в разработке, и не умею это читать")


keyboard = types.InlineKeyboardMarkup() #наша клавиатура
      key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes') #кнопка «Да»
      keyboard.add(key_yes) #добавляем кнопку в клавиатуру
      key_no= types.InlineKeyboardButton(text='Нет', callback_data='no')
      keyboard.add(key_no)
      question = 'Тебе '+str(age)+' лет, тебя зовут '+name+' '+surname+'?'
      bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)'''
name = ''
surname = ''
age = 0



markup = types.ReplyKeyboardMarkup()
itembtna = types.KeyboardButton('ДА')
itembtnb = types.KeyboardButton("НЕТ")

markup.row(itembtna, itembtnb)
with open('names.txt', 'r') as f:
    names = {}
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        if message.from_user.id in names.keys():
            bot.send_message(message.from_user.id, f"Постой, я тебя знаю, {names[message.from_user.id]}, за твою голову назн"
                                                   f"ачена награда!")
        else:
            bot.send_message(message.from_user.id, "Как тебя зовут?", reply_markup=types.ReplyKeyboardRemove(selective=False))
            bot.register_next_step_handler(message, get_name)  # следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg')


def get_name(message):  # получаем фамилию
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, get_age)


def get_age(message):
    global age
    if message.text.isdigit():
        age = int(message.text)  # проверяем, что возраст введен корректно
        bot.send_message(message.from_user.id, f'Тебе {str(age)} лет, тебя зовут {name} {surname} ?', reply_markup=markup)
        bot.register_next_step_handler(message, da_net)
    else:
        bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
        bot.register_next_step_handler(message, get_age)


def da_net(message):
    if message.text=="ДА":
        bot.send_message(message.from_user.id,"MOLODEC", reply_markup=types.ReplyKeyboardRemove(selective=False))
        names[message.from_user.id] = name + " " + surname
        #with open('names.txt', 'r') as f:

        bot.register_next_step_handler(message, start)
    elif message.text=="НЕТ":
        bot.send_message(message.from_user.id, 'Введите имя', reply_markup=types.ReplyKeyboardRemove(selective=False))
        bot.register_next_step_handler(message, get_name)

bot.polling(none_stop=True, interval=0)
