import config
import telebot
import requests

cfg = config.Config('config.cfg')

bot = telebot.TeleBot(cfg['telegram_token'])

url = "https://api.trello.com/1/cards"

from datetime import datetime

query = {
   'key': cfg['trello_key'],
   'token': cfg['trello_token'],
   'idList': cfg['idList'],
   'idBoard': cfg['idBoard']
}

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
	full_message = message.text.split('..')
	if len(full_message) > 1:
		query['name'] = full_message[0]
		query['desc'] = full_message[1]
	else:
		bot.send_message(message.chat.id, 'Возникла проблема. Необходимо передавать данные в формате. "Название карточки".."Описание карточки"')
	response = requests.request(
		"POST",
		url,
		params=query
	)
	if response.status_code == 200:
		bot.send_message(message.chat.id, 'Карточка создана')
	else:
		bot.send_message(message.chat.id, 'Возникла проблема. Карточка не создалась.')

if __name__ == '__main__':
	print('Запущен')
	bot.polling(none_stop=True)