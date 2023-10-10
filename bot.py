import logging
from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
from django.db import transaction
import os
import sys
sys.path.append('/home/cholponklv/Desktop/xacaton/guide/')

# Импортируйте настройки Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "guide.settings")  # Замените на имя вашего проекта Django

import django
django.setup()
from tglocation.models import Locations, TgUser

# Импортируйте библиотеку geopy для расчета расстояния
from geopy.distance import geodesic

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Состояния конечного автомата
LOCATION, ADD_LOCATION, ADD_LOCATION_CONFIRM = range(3)

# Обработчики команды /start
def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    reply_markup = ReplyKeyboardMarkup(
        [[KeyboardButton('Поделиться местоположением', request_location=True)]],
        one_time_keyboard=True
    )
    update.message.reply_text(
        f"Здравствуйте, господин {user.first_name}! Пожалуйста, поделитесь своим местоположением, нажав на кнопку ниже, "
        f"или используйте команду /add_location, чтобы добавить геопозицию места.",
        reply_markup=reply_markup
    )

    return LOCATION

# Обработка полученного местоположения
def receive_location(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_location = update.message.location

    # Сохраняем местоположение пользователя в модели TgUser
    with transaction.atomic():
        tg_user, _ = TgUser.objects.get_or_create(username=user.username)
        tg_user.latitude = str(user_location.latitude)
        tg_user.longitude = str(user_location.longitude)
        tg_user.save()

    reply_markup = ReplyKeyboardMarkup(
        [[KeyboardButton('Пропустить'), KeyboardButton('Добавить место')]],
        one_time_keyboard=True
    )
    update.message.reply_text(
        f"Спасибо, господин {user.first_name}! Ваше местоположение: "
        f"Широта: {user_location.latitude}, Долгота: {user_location.longitude}",
        reply_markup=reply_markup
    )

    return ADD_LOCATION

# Обработка команды "Добавить место"
def add_location(update: Update, context: CallbackContext):
    user = update.message.from_user
    update.message.reply_text(
        f"Господин {user.first_name}, пожалуйста, введите название места, которое вы хотите добавить."
    )

    return ADD_LOCATION_CONFIRM

# Обработка названия места
def receive_location_name(update: Update, context: CallbackContext):
    user = update.message.from_user
    location_name = update.message.text

    # Сохраняем название места в контексте пользователя
    context.user_data['location_name'] = location_name

    update.message.reply_text(
        f"Спасибо, господин {user.first_name}! Теперь поделитесь геопозицией этого места, нажав на кнопку 'Поделиться местоположением'."
    )

    return ADD_LOCATION_CONFIRM

# Обработка геопозиции места и названия
def confirm_add_location(update: Update, context: CallbackContext):
    user = update.message.from_user
    added_location = update.message.location

    # Получаем название места из контекста пользователя
    location_name = context.user_data.get('location_name')

    if not location_name:
        update.message.reply_text("Название места не найдено. Пожалуйста, начните процесс добавления места снова.")
        return ConversationHandler.END

    # Сохраняем местоположение места в модели Locations
    with transaction.atomic():
        tg_user, _ = TgUser.objects.get_or_create(username=user.username)
        Locations.objects.create(
            username=user.first_name,
            name=location_name,
            latitude=str(added_location.latitude),
            longitude=str(added_location.longitude)
        )

    update.message.reply_text(
        f"Спасибо, господин {user.first_name}! Вы успешно добавили место '{location_name}' с геопозицией: "
        f"Широта: {added_location.latitude}, Долгота: {added_location.longitude}"
    )

    # Очищаем данные пользователя из контекста
    context.user_data.clear()

    # Возвращаем состояние ADD_LOCATION, чтобы пользователь мог добавить еще мест
    return ADD_LOCATION

# Функция для завершения диалога
def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("Диалог завершен.")
    return ConversationHandler.END

# Функция для поиска ближайшего местоположения
def find_nearest_location(username):
    try:
        # Получите местоположение пользователя из модели TgUser
        user = TgUser.objects.get(username=username)
        user_location = (float(user.latitude), float(user.longitude))

        # Получите список всех местоположений из модели Locations
        all_locations = Locations.objects.all()

        # Инициализируйте переменные для хранения ближайшего местоположения и минимального расстояния
        nearest_location = None
        min_distance = float('inf')

        # Пройдите по всем местоположениям и найдите ближайшее
        for location in all_locations:
            location_coords = (float(location.latitude), float(location.longitude))
            distance = geodesic(user_location, location_coords).kilometers

            # Если найдено меньшее расстояние, обновите ближайшее местоположение и минимальное расстояние
            if distance < min_distance:
                min_distance = distance
                nearest_location = location

        return nearest_location, min_distance
    except TgUser.DoesNotExist:
        return None, None

# Добавьте обработчик команды для отправки ближайшей геопозиции
def send_nearest_location(update: Update, context: CallbackContext):
    user = update.message.from_user
    username = user.username

    # Вызовите функцию find_nearest_location для поиска ближайшего местоположения
    nearest_location, min_distance = find_nearest_location(username)

    if nearest_location:
        # Отправляем ближайшее местоположение пользователю
        update.message.reply_location(
            latitude=float(nearest_location.latitude),
            longitude=float(nearest_location.longitude),
        )
    else:
        update.message.reply_text("Ваше местоположение не найдено или вы не добавили его.")

def main():
    updater = Updater(token='6505801822:AAHrauG6e9GCXjhslHFsR2okABRvDPJUR7U', use_context=True)  # Замените на ваш токен бота
    dp = updater.dispatcher

    # Создаем обработчики
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LOCATION: [MessageHandler(Filters.location, receive_location)],
            ADD_LOCATION: [
                MessageHandler(Filters.text & Filters.regex('^Добавить место$'), add_location),
                MessageHandler(Filters.text & ~Filters.regex('^Добавить место$'), receive_location_name),
            ],
            ADD_LOCATION_CONFIRM: [MessageHandler(Filters.location, confirm_add_location)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # Добавьте обработчик команды /send_nearest_location
    dp.add_handler(CommandHandler('send_nearest_location', send_nearest_location))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
