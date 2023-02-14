from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton("Go first")
b2 = KeyboardButton("Bot go first")
b3 = KeyboardButton("Stop game")

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb2 = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(b1, b2)
kb2.add(b3)
