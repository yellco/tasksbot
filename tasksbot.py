import config
import telebot

cfg = config.Config('config.cfg')

bot = telebot.TeleBot(cfg['token'])

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    print('Запущен')
    bot.polling(none_stop=True)