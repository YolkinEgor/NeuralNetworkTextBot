from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

select_type_keyboard = InlineKeyboardMarkup()
select_type_keyboard.add(
    InlineKeyboardButton(text='Хоррор',
                         callback_data='horror_stories'),
    InlineKeyboardButton(text='Стихотворный',
                         callback_data='poems'),

)
select_type_keyboard.add(InlineKeyboardButton(text='Шуточный', callback_data='jokes'))
select_type_keyboard.add(InlineKeyboardButton(text='На основе соцсетей',
                                              callback_data='posts'))
