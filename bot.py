import config
import telebot
import re
from telebot import types
from fractions import Fraction

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет, я калькулятор простых и смешаных дробей!'")


@bot.message_handler(content_types=['text'])
def ask_first_argument(message):    # получаем первый аргумент
    bot.send_message(message.from_user.id, "Напиши первый аргумент в формате 'a/b' или 'A b/c'")
    bot.register_next_step_handler(message, convert_first_argument_and_ask_operation)  # следующий шаг – функция first_argument


def convert_first_argument_and_ask_operation(message):
    global first_arg
    # если аргумент соответствует нужному формату и это смешанная дробь, т.е. есть целая часть
    if re.match('[-+]?\d+\s[-+]?\d+\S[-+]?\d+', message.text) is not None:
        integer = int(' '.join([str(i) for i in re.findall(r'^\w+', message.text)]))
        numerator = int(' '.join([str(i) for i in re.findall(r' \w+', message.text)]))
        denominator = int(' '.join([str(i) for i in re.findall(r'\w+$', message.text)]))
        if denominator == 0:
            bot.send_message(message.from_user.id, 'Знаменатель не может быть равен 0')
            bot.register_next_step_handler(message, ask_first_argument)
        else:
            first_arg = Fraction(integer * denominator + numerator, denominator)
            # выводим клавиатуру из 4 кнопок и запрашиваем операцию
            keyboard = types.InlineKeyboardMarkup()
            key_addition = types.InlineKeyboardButton(text='+', callback_data='addition')
            keyboard.add(key_addition)
            key_subtraction = types.InlineKeyboardButton(text='-', callback_data='subtraction')
            keyboard.add(key_subtraction)
            key_multiplication = types.InlineKeyboardButton(text='*', callback_data='multiplication')
            keyboard.add(key_multiplication)
            key_division = types.InlineKeyboardButton(text=':', callback_data='division')
            keyboard.add(key_division)
            bot.send_message(message.from_user.id, text='Выбери операцию', reply_markup=keyboard)
            bot.register_next_step_handler(message, convert_second_argument_and_ask_exit)
    # если аргумент соответствует нужному формату и это простая дробь
    elif re.match('[-+]?\d+\S[-+]?\d+', message.text) is not None:
        numerator = int(' '.join([str(i) for i in re.findall(r'^\w+', message.text)]))
        denominator = int(' '.join([str(i) for i in re.findall(r'\w+$', message.text)]))
        if denominator == 0:
            bot.send_message(message.from_user.id, 'Знаменатель не может быть равен 0')
            bot.register_next_step_handler(message, ask_first_argument)
        else:
            first_arg = Fraction(numerator, denominator)
            # выводим клавиатуру из 4 кнопок и запрашиваем операцию
            keyboard = types.InlineKeyboardMarkup()
            key_addition = types.InlineKeyboardButton(text='+', callback_data='addition')
            keyboard.add(key_addition)
            key_subtraction = types.InlineKeyboardButton(text='-', callback_data='subtraction')
            keyboard.add(key_subtraction)
            key_multiplication = types.InlineKeyboardButton(text='*', callback_data='multiplication')
            keyboard.add(key_multiplication)
            key_division = types.InlineKeyboardButton(text=':', callback_data='division')
            keyboard.add(key_division)
            bot.send_message(message.from_user.id, text='Выбери операцию', reply_markup=keyboard)
            bot.register_next_step_handler(message, convert_second_argument_and_ask_exit)
    else:
        bot.send_message(message.from_user.id, 'Аргумент указан в неправильном формате')
        bot.register_next_step_handler(message, ask_first_argument)


def convert_second_argument_and_ask_exit(message):
    global second_arg
    # если аргумент соответствует нужному формату и это смешанная дробь, т.е. есть целая часть
    if re.match('[-+]?\d+\s[-+]?\d+\S[-+]?\d+', message.text) is not None:
        integer = int(' '.join([str(i) for i in re.findall(r'^\w+', message.text)]))
        numerator = int(' '.join([str(i) for i in re.findall(r' \w+', message.text)]))
        denominator = int(' '.join([str(i) for i in re.findall(r'\w+$', message.text)]))
        if denominator == 0:
            bot.send_message(message.from_user.id, 'Знаменатель не может быть равен 0')
        else:
            second_arg = Fraction(integer * denominator + numerator, denominator)
        keyboard = types.InlineKeyboardMarkup()
        key_equality = types.InlineKeyboardButton(text='=', callback_data='equality')
        keyboard.add(key_equality)
        bot.send_message(message.from_user.id, text='Получить ответ', reply_markup=keyboard)
    # если аргумент соответствует нужному формату и это простая дробь
    elif re.match('[-+]?\d+\S[-+]?\d+', message.text) is not None:
        numerator = int(' '.join([str(i) for i in re.findall(r'^\w+', message.text)]))
        denominator = int(' '.join([str(i) for i in re.findall(r'\w+$', message.text)]))
        if denominator == 0:
            bot.send_message(message.from_user.id, 'Знаменатель не может быть равен 0')
        else:
            second_arg = Fraction(numerator, denominator)
        keyboard = types.InlineKeyboardMarkup()
        key_equality = types.InlineKeyboardButton(text='=', callback_data='equality')
        keyboard.add(key_equality)
        bot.send_message(message.from_user.id, text='Получить ответ', reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, 'Аргумент указан в неправильном формате')
        bot.register_next_step_handler(message, ask_first_argument)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global oper
    # обработчик кнопок
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
            res = first_arg+second_arg
        elif oper == 'subtraction':
            res = first_arg-second_arg
        elif oper == 'multiplication':
            res = first_arg*second_arg
        elif oper == 'division':
            if second_arg.numerator == 0:
                bot.send_message(call.message.chat.id, 'Делить на 0 нельзя!')
                bot.register_next_step_handler(message, ask_first_argument)
            else:
                res = first_arg/second_arg
        # формируем ответ
        if res.numerator//res.denominator == 0 and res.numerator == 0:
            answer = '0'
        elif res.numerator//res.denominator == 0 and res.numerator != 0:
            answer = str(res.numerator) + '/' + str(res.denominator)
        elif res.numerator//res.denominator != 0 and res.numerator%res.denominator == 0:
            answer = str(res.numerator // res.denominator)
        elif res.numerator//res.denominator != 0 and res.numerator%res.denominator != 0:
            answer = str(res.numerator // res.denominator) + ' ' + str(res.numerator % res.denominator) + '/' + str(res.denominator)
        bot.send_message(call.message.chat.id, 'Ответ: '+answer)


if __name__ == '__main__':
     bot.infinity_polling()
