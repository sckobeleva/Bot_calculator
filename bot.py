import config
import telebot
from telebot import types

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет!")


@bot.message_handler(content_types=['text'])
def say_hello(message):    # получаем первый аргумент
    bot.send_message(message.from_user.id, "Напиши первый аргумент")
    bot.register_next_step_handler(message, first_argument_and_operation)  # следующий шаг – функция first_argument


def first_argument_and_operation(message):    # получаем первый аргумент
    global first
    a = message.text.isdigit()
    while a is not True:
        bot.send_message(message.from_user.id, "Напиши первый аргумент, он должен быть числом")
        break
    else:
        first = message.text
        #bot.send_message(message.from_user.id, 'Напиши операцию')
        # bot.send_message(message.from_user.id, first) # проверка, что сохраняется правильное последнее значение
        keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
        key_addition = types.InlineKeyboardButton(text='+', callback_data='addition')  # кнопка «Да»
        keyboard.add(key_addition)  # добавляем кнопку в клавиатуру
        key_subtraction = types.InlineKeyboardButton(text='-', callback_data='subtraction')
        keyboard.add(key_subtraction)
        key_multiplication = types.InlineKeyboardButton(text='*', callback_data='multiplication')
        keyboard.add(key_multiplication)
        key_division = types.InlineKeyboardButton(text=':', callback_data='division')
        keyboard.add(key_division)
        # Показываем все кнопки сразу и пишем сообщение о выборе
        bot.send_message(message.from_user.id, text='Выбери операцию', reply_markup=keyboard)
        bot.register_next_step_handler(message, second_argument_and_operation)


def second_argument_and_operation(message):    # получаем второй аргумент
    global second
    b = message.text.isdigit()
    while b is not True:
        bot.send_message(message.from_user.id, "Напиши второй аргумент, он должен быть числом")
        break
    else:
        second = message.text
        #bot.send_message(message.from_user.id, 'Напиши операцию')
        # bot.send_message(message.from_user.id, first) # проверка, что сохраняется правильное последнее значение
        keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
        key_equality = types.InlineKeyboardButton(text='=', callback_data='equality')  # кнопка «Да»
        keyboard.add(key_equality)  # добавляем кнопку в клавиатуру
        # Показываем все кнопки сразу и пишем сообщение о выборе
        bot.send_message(message.from_user.id, text='Нажми равно', reply_markup=keyboard)
        #bot.register_next_step_handler(message, operation)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global oper
    if call.data == "addition": #call.data это callback_data, которую мы указали при объявлении кнопки
        oper = 'addition'
        bot.send_message(call.message.chat.id, 'Напиши второй аргумент')
    elif call.data == "subtraction":
        oper = 'subtraction'
        bot.send_message(call.message.chat.id, 'Напиши второй аргумент')
    elif call.data == "multiplication":
        oper = 'multiplication'
        bot.send_message(call.message.chat.id, 'Напиши второй аргумент')
    elif call.data == "division":
        oper = 'division'
        bot.send_message(call.message.chat.id, 'Напиши второй аргумент')
    elif call.data == "equality":
        if oper == 'addition':
            res = int(first) + int(second)
        elif oper == 'subtraction':
            res = int(first) - int(second)
        elif oper == 'multiplication':
            res = int(first) * int(second)
        elif oper == 'division':
            res = int(first) / int(second)
        bot.send_message(call.message.chat.id, 'Ответ: '+str(res))


if __name__ == '__main__':
     bot.infinity_polling()
