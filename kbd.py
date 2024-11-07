from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

start_kbd_admin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Статистика'),
            KeyboardButton(text='Список HR'),
        ],
        [
            KeyboardButton(text='Принять заявку')
        ]
    ],
    resize_keyboard=True
)

cansel = [
    [InlineKeyboardButton(text='закрыть', callback_data='cansel_add_hr')]
]
cansel_add_hr = InlineKeyboardMarkup(inline_keyboard=cansel)

k = [
    [InlineKeyboardButton(text='Добавить HR', callback_data='add_hr')],
    [InlineKeyboardButton(text='Очистить список', callback_data='clear_hr')]
]
add_hr = InlineKeyboardMarkup(inline_keyboard=k)

x = [
    [InlineKeyboardButton(text='Назад', callback_data='go_around')]
]
go_around = InlineKeyboardMarkup(inline_keyboard=x)