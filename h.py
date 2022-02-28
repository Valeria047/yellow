from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
import requests
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import random

def echo(update, context):
    global updater, toponym_address
    t = update.message.text
    q = load_map(t)
    if q:
        photo = open('map.png', 'rb')
        updater.bot.send_photo(chat_id=update.message.chat_id, photo=photo, caption=toponym_address)
    else:
        update.message.reply_text("Ничего не найдено")

def load_map(name):
    global toponym_address
    response = requests.get(
        "https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=%s&format=json" % (name))
    try:
        if response:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            toponym_coodrinates = toponym["Point"]["pos"].split()
            toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
            x, y = float(toponym_coodrinates[0]), float(toponym_coodrinates[1])
            map_request = "http://static-maps.yandex.ru/1.x/?ll={}&z={}&l={}&pt={},{},pm2rdl".format(
                str(x) + ',' + str(y), 19, "map", x, y)
            #map_request = "https://static-maps.yandex.ru/1.x/?l=map&pl=%s,%s" % (x, y)
            response = requests.get(map_request)
            if not response:
                print("Ошибка выполнения запроса:")
                print(map_request)
                return
            else:
                map_file = "map.png"
                with open(map_file, "wb") as file:
                    file.write(response.content)
                return map_file

        else:
            print("Ошибка выполнения")
    except:
        return

def remove_job_if_exists(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

def start(update, context):
    update.message.reply_text(
        "Привет! Я Бот-геокодер. Введите объект")

def set_timer(update, context):
    """Добавляем задачу в очередь"""
    chat_id = update.message.chat_id
    try:
        # args[0] должен содержать значение аргумента
        # (секунды таймера)
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text(
                'Извините, не умеем возвращаться в прошлое')
            return
        job_removed = remove_job_if_exists(
            str(chat_id),
            context
        )
        context.job_queue.run_once(
            task,
            due,
            context=chat_id,
            name=str(chat_id)
        )
        text = f'Вернусь через {due} секунд!'
        if job_removed:
            text += ' Старая задача удалена.'
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Использование: /set <секунд>')

def task(context):
    job = context.job
    context.bot.send_message(job.context, text='30 сенкунд истекли!')


def unset_timer(update, context):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Хорошо, вернулся сейчас!' if job_removed else 'Нет активного таймера.'
    update.message.reply_text(text)


def go(update, context):
    global answer, kol_false, kol_true, a
    a_copy = a[:]
    kol_false, kol_true = 0, 0
    n = random.randint(0, len(a_copy) - 1)
    que = a_copy[n]
    answer = d[que]
    update.message.reply_text(
        que,
        reply_markup=ReplyKeyboardRemove()
    )
    del a_copy[n]

def close(update, context):
    update.message.reply_text(
        ")))",
        reply_markup=ReplyKeyboardRemove()
    )
    return


def main():
    global updater
    updater = Updater("5216629633:AAFJLT1CWG_a_rFoxztI2Gta7cIbPpKKZm0", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("set_timer", set_timer,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("stop", close))
    dp.add_handler(CommandHandler("go", go))
    dp.add_handler(CommandHandler("unset", unset_timer, pass_chat_data=True))
    text_handler = MessageHandler(Filters.text, echo)

    # Регистрируем обработчик в диспетчере.
    dp.add_handler(text_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()