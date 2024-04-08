import telebot
import json

TOKEN = '7160653437:AAHQ_msKwuvBNZcFNpCYG0ZRRnnGnSmGawU'
bot = telebot.TeleBot(TOKEN)
settings = open('settings.txt', 'r').read()
settings = json.loads(settings)

