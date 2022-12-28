from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


only_back = InlineKeyboardMarkup(keyboard=[
    [
        InlineKeyboardButton(
            text='⬅️ назад',
            callback_data='back_to_rent_menu'
        )
    ]
])