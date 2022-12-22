from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


start_rent_markup = InlineKeyboardMarkup(keyboard=[
    [
        InlineKeyboardButton(
            text='создать бота',
            callback_data='rent_new_bot'
        ),
        InlineKeyboardButton(
            text='изменить бота',
            callback_data='get_bots_change_menu'
        )
    ],
    [
        InlineKeyboardButton(
            text='ссылки на ботов',
            callback_data='get_bots_urls_menu'
        )  
    ],
    [
        InlineKeyboardButton(
            text='оплатить подписку',
            callback_data='pay for a subscription'
        ),
        InlineKeyboardButton(
            text='мой аккаунт',
            callback_data='get_account'
        )
    ],
    [
        InlineKeyboardButton(
            text='faq',
            callback_data='get_faq'
        )
    ]
])

only_back = InlineKeyboardMarkup(keyboard=[
    [
        InlineKeyboardButton(
            text='⬅️ назад',
            callback_data='back_to_rent_menu'
        )
    ]
])