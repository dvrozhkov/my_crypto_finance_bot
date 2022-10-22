import telebot
import read

API_KEY = "your token"
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     "Привет! Меня зовут @my_crypto_finance_bot! Я могу"
                     " помочь с поиском криптовалюты, изменением стоимости,"
                     " объемом и многим другим! Введи название криптовалюты,"
                     " которая тебя интересует!")

@bot.message_handler(content_types=['text'])
def send_crypto_info(message):
    found = False
    crypto_set = read.read_crypto()
    i_count = -1
    for i in crypto_set:
        i_count += 1
        if message.text.lower() in i.name.lower() or message.text.lower() in i.iname.lower():
            markup = telebot.types.InlineKeyboardMarkup(row_width=2)
            markup.add(telebot.types.InlineKeyboardButton(text='Подробнее', callback_data=str(i_count)))
            markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data=str(-1)))
            bot.send_message(message.chat.id,
                             f"**{i.name}** ({i.iname})\n"
                             f"Стоимость: {i.cost} ({i.rise_in_cost})\n"
                             f"Капитализация: {i.capitalisation}\n"
                             f"Объем (24ч.): {i.volume}\n"
                             f"Изменеиния (24ч.): {i.changes}", reply_markup=markup)
            found = True
            break
    if not found:
        bot.send_message(message.chat.id, "Я не могу найти то, что вы запрашиваете!"
                                          " Попробуйте ввести название подругому.")

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id, text='Загрузка')
    answer = ''
    if call.data == '-1':
        answer = 'Введите любое название криптовалюты!'
        bot.send_message(call.message.chat.id, answer)
    else:
        crypto_set = read.read_crypto()
        answer = ""
        print(int(call.data))
        for k, v in crypto_set[int(call.data)].more_info.items():
            if str(k) == "0":
                answer += f"Актуальность: {v[27::]}\n"
            else:
                answer += f"{k}: {v}\n"
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data=str(-1)))
        bot.send_message(call.message.chat.id, answer, reply_markup=markup)


bot.polling(none_stop=True)
