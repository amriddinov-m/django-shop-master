import time
import telepot

from conf import BOT_TOKEN, ADMIN_ID, ORDER_URI
from dsshop.celery import app
bot = telepot.Bot(BOT_TOKEN)


@app.task
def send_order(text):
    # txt = "Поступил новый заказ. Ссылка на заказ " + ORDER_URI + " " + str(order_id)
    for user_id in ADMIN_ID:
        try:
            bot.sendMessage(user_id, text, parse_mode='HTML')
        except:
            pass
