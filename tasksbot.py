import config
import telebot
import requests

cfg = config.Config('config.cfg')

bot = telebot.TeleBot(cfg['telegram_token'])

url = "https://api.trello.com/1/cards"

from datetime import datetime

query = {
   'key': cfg['trello_key'],
   'token': '',
   'idList': cfg['idList'],
   'idBoard': cfg['idBoard']
}

token = ''

def create_board():
	global token
	url = "https://api.trello.com/1/boards/"

	query = {
		'key': cfg['trello_key'],
		'token': token,
		'name': 'Tasksbot доска'
	}

	response = requests.request(
		"POST",
		url,
		params=query
	)

	print(response.text)

@bot.message_handler(commands=['start'])
def handle_start(message):
	bot.send_message(message.chat.id, "Привет. Для начала давай настроим приложение. ")
	keyboard = telebot.types.InlineKeyboardMarkup()
	url_button = telebot.types.InlineKeyboardButton(text="Авторизация trello", url="https://trello.com/1/authorize?expiration=1day&name=Telegram tasksbot&scope=read,write,account&response_type=token&key=" + cfg['trello_key'])
	keyboard.add(url_button)
	bot.send_message(message.chat.id, "Сначала авторизуй приложение по ссылке и пришли мне токен.", reply_markup=keyboard)

@bot.message_handler(content_types=["text"])
def check_messages(message):
	global token
	if len(query['token']) > 0:
		full_message = message.text.split('..')
		print(full_message)
		if len(full_message) > 1:
			query['name'] = full_message[0]
			query['desc'] = full_message[1]

			response = requests.request(
				"POST",
				url,
				params=query
			)
			print(response.text)
			if response.status_code == 200:
				bot.send_message(message.chat.id, 'Карточка создана')
			else:
				bot.send_message(message.chat.id, 'Возникла проблема. Карточка не создалась.')
		else:
			bot.send_message(message.chat.id, 'Возникла проблема. Необходимо передавать данные в формате. "Название карточки..Описание карточки"')
	elif len(query['token']) == 0:
		if len(message.text) == 64:
			bot.send_message(message.chat.id, 'Token принят. Давай создадим новую доску.')
			# create_board()
			query['token'] = message.text
			token = message.text
			# bot.send_message(message.chat.id, 'Теперь пришли мне id доски куда хочешь слать карточки.')
		else:
			keyboard = telebot.types.InlineKeyboardMarkup()
			auth_button = telebot.types.InlineKeyboardButton(text="Авторизация trello", url="https://trello.com/1/authorize?expiration=1day&name=Telegram tasksbot&scope=read,write&response_type=token&key=" + cfg['trello_key'])
			keyboard.add(auth_button)
			bot.reply_to(message, "Проверь свой токен и пришли мне его ещё раз.", reply_markup=keyboard)

if __name__ == '__main__':
	print('Запущен')
	bot.polling(none_stop=True)