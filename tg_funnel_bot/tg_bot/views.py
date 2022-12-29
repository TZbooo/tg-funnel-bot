import django.utils.timezone as tz
from django.conf import settings
from django.contrib.auth import get_user_model
from telebot.types import Update
from telebot.apihelper import ApiTelegramException
from rest_framework.views import APIView
from rest_framework.response import Response
from celery import shared_task

from tg_funnel_bot.bot import bot
from tg_funnel_bot.stripe import stripe
from .models import TelegramBotClientModel
from .utils import get_bot_command_argument

from .handlers.rent import (
    start_rent,
    get_bots_change_menu,
    get_bots_urls_menu,
    back_to_rent_menu,
    start_rent_new_bot,
    get_account,
    pay_for_bot
)
from .handlers.client import (
    start_funnel_dialog,
    first_question_handler,
    second_question_handler,
    tg_nick_or_phone_input_handler
)


# funnel dialog handlers
bot.register_message_handler(
    callback=start_funnel_dialog,
    commands=['start'],
    func=lambda message: get_bot_command_argument(message)
)
bot.register_callback_query_handler(
    callback=first_question_handler,
    func=lambda query: 'start' in query.data
)
bot.register_callback_query_handler(
    callback=second_question_handler,
    func=lambda query: 'first' in query.data
)

# rent menu handlers
bot.register_message_handler(
    callback=start_rent,
    commands=['start'],
    func=lambda message: get_bot_command_argument(message) is None
)
bot.register_callback_query_handler(
    callback=get_bots_change_menu,
    func=lambda query: query.data == 'get_bots_change_menu'
)
bot.register_callback_query_handler(
    callback=get_bots_urls_menu,
    func=lambda query: query.data == 'get_bots_urls_menu'
)
bot.register_callback_query_handler(
    callback=back_to_rent_menu,
    func=lambda query: query.data == 'back_to_rent_menu'
)
bot.register_callback_query_handler(
    callback=start_rent_new_bot,
    func=lambda query: query.data == 'rent_new_bot'
)
bot.register_callback_query_handler(
    callback=get_account,
    func=lambda query: query.data == 'get_account'
)
bot.register_callback_query_handler(
    callback=pay_for_bot,
    func=lambda query: query.data == 'pay_for_bot'
)


class TelegramUpdatesAPIView(APIView):
    def post(self, request):
        json_data = request.body.decode('UTF-8')
        update_data = Update.de_json(json_data)
        bot.process_new_updates([update_data])
        
        if update_data.message:
            no_nick_or_phone_clients = TelegramBotClientModel.objects.filter(
                chat_id=update_data.message.chat.id,
                phone_or_nickname=None
            ).exclude(
                sent_messages_for_inactive_count=0
            )

            if no_nick_or_phone_clients.exists():
                no_nick_or_phone_clients.update(sent_messages_for_inactive_count=0)
                tg_nick_or_phone_input_handler(update_data.message)

        return Response(status=200)


class StripeUpdatesAPIView(APIView):
    def post(self, request):
        event = None
        payload = request.body.decode('utf-8')
        if settings.STRIPE_ENDPOINT_SECRET:
            sig_header = request.headers.get('stripe-signature')
            try:
                event = stripe.Webhook.construct_event(
                    payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
                )
            except stripe.error.SignatureVerificationError as e:
                return Response(status=400)

        if event['type'] == 'checkout.session.completed':
            payment_method = event['data']['object']
            bots_owner_chat_id = payment_method['metadata']['bots_owner_id']
            print(bots_owner_chat_id)
            print(event['data'])
            User = get_user_model()
            User.objects.get(
                owner_chat_id=bots_owner_chat_id
            ).switch_to_paid_rate().save()
            bot.send_message(
                chat_id=bots_owner_chat_id,
                text='спасибо, что оформили платную подписку'
            )

        return Response(status=200)


@shared_task(name='send_certain_messages_for_inactive_users')
def send_certain_messages_for_inactive_users():
    no_nick_or_phone_clients = TelegramBotClientModel.objects.filter(
        phone_or_nickname=None
    )
    inactive_for_two_days_clients = no_nick_or_phone_clients.filter(
        updated_at__lte=tz.now() - tz.timedelta(minutes=5),
        sent_messages_for_inactive_count=2
    )
    inactive_for_day_clients = no_nick_or_phone_clients.filter(
        updated_at__lte=tz.now() - tz.timedelta(minutes=3),
        sent_messages_for_inactive_count=1
    ).difference(inactive_for_two_days_clients)
    inactive_for_hour_clients = no_nick_or_phone_clients.filter(
        updated_at__lte=tz.now() - tz.timedelta(minutes=2),
        sent_messages_for_inactive_count=0
    ).difference(inactive_for_day_clients)

    for inactive_client in inactive_for_hour_clients:
        for bot_settings in inactive_client.bots.all():
            chat_id = inactive_client.chat_id
            try:
                bot.send_message(
                    chat_id=chat_id,
                    text=bot_settings.user_inactive_for_hour_message_text_first_part
                )
                bot.send_message(
                    chat_id=chat_id,
                    text=bot_settings.user_inactive_for_hour_message_text_second_part,
                    reply_markup=bot_settings.get_inactive_message_markup()
                )
            except ApiTelegramException as e:
                print(e)
            inactive_client.sent_messages_for_inactive_count += 1
            inactive_client.save()

    for inactive_client in inactive_for_day_clients:
        for bot_settings in inactive_client.bots.all():
            chat_id = inactive_client.chat_id
            try:
                bot.send_message(
                    chat_id=chat_id,
                    text=bot_settings.user_inactive_for_day_message_text_first_part,
                    reply_markup=bot_settings.get_inactive_message_markup()
                )
                bot.send_message(
                    chat_id=chat_id,
                    text=bot_settings.user_inactive_for_day_message_text_second_part
                )
            except ApiTelegramException as e:
                print(e)
            inactive_client.sent_messages_for_inactive_count += 1
            inactive_client.save()

    for inactive_client in inactive_for_two_days_clients:
        for bot_settings in inactive_client.bots.all():
            chat_id = inactive_client.chat_id
            try:
                bot.send_message(
                    chat_id=chat_id,
                    text=bot_settings.user_inactive_for_two_days_message_text
                )
            except ApiTelegramException as e:
                print(e)
            inactive_client.sent_messages_for_inactive_count += 1
            inactive_client.save()
    return tz.now()