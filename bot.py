import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
import os
import sys
sys.path.append('/home/cholponklv/Desktop/xacaton/guide/')

# Импортируйте настройки Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "guide.settings")  # Замените на ваше имя проекта

import django
django.setup()
from tglocation.models import Locations ,TgUser

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Определение состояний для конечного автомата
ADD_LOCATION, SAVE_LOCATION = range(2)

# Создаем функцию-обработчик команды /start
def start(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    update.message.reply_html(
        fr"Привет, {user.mention_html()}!"
        "\n\n"
        "Я бот, который может сохранять местоположение пользователя. "
        "Чтобы отправить свое местоположение, нажмите кнопку 'Отправить местоположение' ниже."
        "\n\n"
        "Или используйте команду /add для добавления других мест."
    )

    # Создаем клавиатуру с кнопкой "Отправить местоположение"
    keyboard = [[InlineKeyboardButton("Отправить местоположение", callback_data='send_location')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Или нажмите кнопку ниже, чтобы отправить местоположение:", reply_markup=reply_markup)

    return ADD_LOCATION

# Создаем функцию-обработчик для запроса местоположения через Callback
def location_callback(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    user = query.message.chat
    query.answer()

    # Отправляем запрос на местоположение
    query.message.reply_text("Пожалуйста, отправьте ваше текущее местоположение.")

    return SAVE_LOCATION

# Создаем функцию-обработчик для получения и сохранения местоположения пользователя
def save_location(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude

    # Сохраняем местоположение в модели TgUser
    tg_user, created = TgUser.objects.get_or_create(username=user.username)
    tg_user.latitude = str(latitude)
    tg_user.longitude = str(longitude)
    tg_user.save()

    update.message.reply_text("Ваше местоположение успешно сохранено!")

    return ConversationHandler.END

# Создаем функцию-обработчик для добавления других мест
def add_location(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    update.message.reply_text("Пожалуйста, отправьте местоположение, которое вы хотите сохранить в виде точки на карте.")
    context.user_data["adding_location"] = True  # Устанавливаем флаг добавления места

    return SAVE_LOCATION

# Создаем функцию-обработчик для сохранения местоположения в модели Locations
def save_custom_location(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    location = update.message.location

    # Получаем название места от пользователя
    location_name = context.args[0] if context.args else "Неизвестное место"

    # Сохраняем местоположение в модели Locations
    location_obj = Locations(
        username=user.username,
        name=location_name,
        latitude=str(location.latitude),
        longitude=str(location.longitude)
    )
    location_obj.save()

    update.message.reply_text(f"Место '{location_name}' успешно сохранено в Locations!")

    return ConversationHandler.END

# Основная функция для запуска бота
def main():
    # Инициализируем бота
    updater = Updater("YOUR_BOT_TOKEN", use_context=True)

    # Получаем объект диспетчера для регистрации обработчиков
    dp = updater.dispatcher

    # Регистрируем обработчики команд и сообщений
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ADD_LOCATION: [CallbackQueryHandler(location_callback, pattern='send_location')],
            SAVE_LOCATION: [MessageHandler(Filters.location & ~Filters.command, save_location)],
        },
        fallbacks=[]
    )
    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("add", add_location))
    dp.add_handler(CommandHandler("save", save_custom_location, pass_args=True))

    # Запускаем бота
    updater.start_polling()

    # Запускаем бота и ожидаем завершения
    updater.idle()

if __name__ == '__main__':
    main()