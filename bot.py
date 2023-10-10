from geopy.distance import geodesic
from tglocation.models import Locations, TgUser
import django
import logging
from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
from django.db import transaction
import os
import sys
import time
import uuid

sys.path.append('/home/cholponklv/Desktop/xacaton/guide/')


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "guide.settings")

django.setup()


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


LOCATION, ADD_LOCATION, ADD_LOCATION_CONFIRM, ADD_LOCATION_CONFIRM_NAME, ADD_LOCATION_PHOTO = range(5)


def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    reply_markup = ReplyKeyboardMarkup(
        [[KeyboardButton('Поделиться местоположением',
                         request_location=True)]],
        one_time_keyboard=True
    )
    update.message.reply_text(
        f"Здравствуйте, господин {user.first_name}! Пожалуйста, поделитесь своим местоположением, нажав на кнопку ниже, "
        f"или используйте команду /add_location, чтобы добавить геопозицию места.",
        reply_markup=reply_markup
    )

    return LOCATION


def receive_location(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_location = update.message.location

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


def add_location(update: Update, context: CallbackContext):
    user = update.message.from_user
    update.message.reply_text(
        f"Господин {user.first_name}, чтобы добавить место, поделитесь геопозицией этого места, нажав на кнопку 'Поделиться местоположением'."
    )

    return ADD_LOCATION_CONFIRM


def confirm_add_location(update: Update, context: CallbackContext):
    user = update.message.from_user
    added_location = update.message.location

    context.user_data['temp_location'] = added_location

    update.message.reply_text(f"Пожалуйста, введите название места:")

    return ADD_LOCATION_CONFIRM_NAME


def receive_location_name(update: Update, context: CallbackContext):
    user = update.message.from_user
    location_name = update.message.text[:100]

    added_location = context.user_data['temp_location']

    context.user_data['temp_location_name'] = location_name

    update.message.reply_text(f"Пожалуйста, прикрепите фотографию места:")

    return ADD_LOCATION_PHOTO


def receive_location_photo(update: Update, context: CallbackContext):
    user = update.message.from_user
    location_name = context.user_data.get('temp_location_name')
    added_location = context.user_data.get('temp_location')

    if update.message.photo:

        unique_filename = f"{int(time.time())}_{uuid.uuid4().hex}.jpg"

        photo = update.message.photo[-1].file_id

        file = context.bot.get_file(photo)

        file.download(custom_path=f'media/{unique_filename}')

        with transaction.atomic():
            Locations.objects.create(
                username=user.first_name,
                name=location_name,
                latitude=str(added_location.latitude),
                longitude=str(added_location.longitude),
                photo=f'{unique_filename}'
            )

        update.message.reply_text(
            f"Спасибо, господин {user.first_name}! Вы поделились местоположением места '{location_name}' и прикрепили фотографию."
        )
    else:
        update.message.reply_text(
            "Вы не прикрепили фотографию. Пожалуйста, прикрепите фотографию места.")

    return ADD_LOCATION


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("Диалог завершен.")
    return ConversationHandler.END


def find_next_nearest_location(username, sent_locations):
    try:

        user = TgUser.objects.get(username=username)
        user_location = (float(user.latitude), float(user.longitude))

        all_locations = Locations.objects.exclude(id__in=sent_locations)

        nearest_location = None
        min_distance = float('inf')

        for location in all_locations:
            location_coords = (float(location.latitude),
                               float(location.longitude))
            distance = geodesic(user_location, location_coords).kilometers

            if distance < min_distance:
                min_distance = distance
                nearest_location = location

        return nearest_location, min_distance
    except TgUser.DoesNotExist:
        return None, None


def send_nearest_location(update: Update, context: CallbackContext):
    user = update.message.from_user
    username = user.username

    if 'sent_locations' not in context.user_data:
        context.user_data['sent_locations'] = []

    nearest_location, min_distance = find_next_nearest_location(
        username, context.user_data['sent_locations'])

    if nearest_location:

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

        context.user_data['sent_locations'].append(nearest_location.id)
    else:
        update.message.reply_text(
            "Ваше местоположение не найдено или вы не добавили его.")


def main():
    updater = Updater(token='6505801822:AAHrauG6e9GCXjhslHFsR2okABRvDPJUR7U',
                      use_context=True)  # Замените на ваш токен бота
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LOCATION: [MessageHandler(Filters.location, receive_location)],
            ADD_LOCATION: [MessageHandler(Filters.text & Filters.regex('^Добавить место$'), add_location)],
            ADD_LOCATION_CONFIRM: [MessageHandler(Filters.location, confirm_add_location)],
            ADD_LOCATION_CONFIRM_NAME: [MessageHandler(Filters.text, receive_location_name)],
            ADD_LOCATION_PHOTO: [MessageHandler(
                Filters.photo, receive_location_photo)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    dp.add_handler(CommandHandler(
        'send_nearest_location', send_nearest_location))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
