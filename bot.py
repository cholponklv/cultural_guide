import logging
from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
from django.db import transaction
import os
import sys
import time
import uuid

sys.path.append('/home/cholponklv/Desktop/xacaton/guide/')

# Импортируйте настройки Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "guide.settings")

import django
django.setup()
from tglocation.models import Locations, TgUser

# Импортируйте библиотеку geopy для расчета расстояния
from geopy.distance import geodesic

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Состояния конечного автомата
LOCATION, ADD_LOCATION, ADD_LOCATION_CONFIRM, ADD_LOCATION_CONFIRM_NAME, ADD_LOCATION_PHOTO = range(5)

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

# Обработка команды "Добавить место" с возможностью добавления фотографии
def add_location(update: Update, context: CallbackContext):
    user = update.message.from_user
    update.message.reply_text(
        f"Господин {user.first_name}, чтобы добавить место, поделитесь геопозицией этого места, нажав на кнопку 'Поделиться местоположением'."
    )

    return ADD_LOCATION_CONFIRM

# Обработка геопозиции места и запрос названия
def confirm_add_location(update: Update, context: CallbackContext):
    user = update.message.from_user
    added_location = update.message.location

    # Сохраняем местоположение места в контексте пользователя
    context.user_data['temp_location'] = added_location

    # Запрашиваем название места
    update.message.reply_text(f"Пожалуйста, введите название места:")

    return ADD_LOCATION_CONFIRM_NAME

# Обработка введенного названия места и запрос фотографии
def receive_location_name(update: Update, context: CallbackContext):
    user = update.message.from_user
    location_name = update.message.text[:100]  # Обрезаем название места до 100 символов, если оно слишком длинное


    # Получаем временное местоположение из контекста пользователя
    added_location = context.user_data['temp_location']

    # Сохраняем название места в контексте пользователя
    context.user_data['temp_location_name'] = location_name

    # Запрашиваем фотографию места
    update.message.reply_text(f"Пожалуйста, прикрепите фотографию места:")

    return ADD_LOCATION_PHOTO

# Обработка прикрепленной фотографии и сохранение места с названием и фотографией
def receive_location_photo(update: Update, context: CallbackContext):
    user = update.message.from_user
    location_name = context.user_data.get('temp_location_name')
    added_location = context.user_data.get('temp_location')

    # Проверяем, что фотография прикреплена к сообщению
    if update.message.photo:
    # Генерируем уникальное имя файла, например, на основе текущего времени

        unique_filename = f"{int(time.time())}_{uuid.uuid4().hex}.jpg"

        # Получаем фотографию с наибольшим разрешением
        photo = update.message.photo[-1].file_id

        # Получаем объект фотографии с помощью API бота
        file = context.bot.get_file(photo)

        # Загружаем фотографию на диск, указав уникальное имя файла
        file.download(custom_path=f'media/{unique_filename}')

        # Сохраняем местоположение места в модели Locations вместе с названием и уникальным именем фотографии
        with transaction.atomic():
            Locations.objects.create(
                username=user.first_name,
                name=location_name,
                latitude=str(added_location.latitude),
                longitude=str(added_location.longitude),
                photo=f'{unique_filename}'  # Сохраняем путь к уникальной фотографии
            )

        update.message.reply_text(
            f"Спасибо, господин {user.first_name}! Вы поделились местоположением места '{location_name}' и прикрепили фотографию."
        )
    else:
        update.message.reply_text("Вы не прикрепили фотографию. Пожалуйста, прикрепите фотографию места.")

    # Возвращаем состояние ADD_LOCATION, чтобы пользователь мог добавить еще мест
    return ADD_LOCATION

# Функция для завершения диалога
def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("Диалог завершен.")
    return ConversationHandler.END

# Функция для поиска ближайшего местоположения
def find_next_nearest_location(username, sent_locations):
    try:
        # Получите местоположение пользователя из модели TgUser
        user = TgUser.objects.get(username=username)
        user_location = (float(user.latitude), float(user.longitude))

        # Получите список всех местоположений из модели Locations, исключая уже отправленные
        all_locations = Locations.objects.exclude(id__in=sent_locations)

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


def send_nearest_location(update: Update, context: CallbackContext):
    user = update.message.from_user
    username = user.username

    # Проверяем, есть ли уже список отправленных мест в контексте пользователя, если нет, то создаем его
    if 'sent_locations' not in context.user_data:
        context.user_data['sent_locations'] = []

    # Вызываем функцию find_nearest_location для поиска ближайшего местоположения, но исключаем уже отправленные
    nearest_location, min_distance = find_next_nearest_location(username, context.user_data['sent_locations'])

    if nearest_location:
        # Отправляем ближайшее местоположение пользователю с названием, геопозицией, расстоянием и фотографией
        update.message.reply_text(
            f"Ближайшее место: {nearest_location.name}\n"
            f"Геопозиция: Широта: {float(nearest_location.latitude)}, Долгота: {float(nearest_location.longitude)}\n"
            f"Расстояние: {min_distance:.2f} км"
        )
        update.message.reply_photo(
            photo=nearest_location.photo,
            caption=f"Фотография места '{nearest_location.name}'"
        )
        update.message.reply_location(
            latitude=float(nearest_location.latitude),
            longitude=float(nearest_location.longitude),
        )

        # Добавляем отправленное место в список отправленных в контексте пользователя
        context.user_data['sent_locations'].append(nearest_location.id)
    else:
        update.message.reply_text("Ваше местоположение не найдено или вы не добавили его.")


# Внесите изменения в функцию main() для добавления обработчика команды /send_nearest_location
def main():
    updater = Updater(token='6505801822:AAHrauG6e9GCXjhslHFsR2okABRvDPJUR7U', use_context=True)  # Замените на ваш токен бота
    dp = updater.dispatcher

    # Создаем обработчики
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LOCATION: [MessageHandler(Filters.location, receive_location)],
            ADD_LOCATION: [MessageHandler(Filters.text & Filters.regex('^Добавить место$'), add_location)],
            ADD_LOCATION_CONFIRM: [MessageHandler(Filters.location, confirm_add_location)],
            ADD_LOCATION_CONFIRM_NAME: [MessageHandler(Filters.text, receive_location_name)],
            ADD_LOCATION_PHOTO: [MessageHandler(Filters.photo, receive_location_photo)]
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
