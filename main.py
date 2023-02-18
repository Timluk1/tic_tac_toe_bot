from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, Dispatcher, StatesGroup
from aiogram import types
import button
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton
import os

def spaceIsFree(position):
    if board[position] == '__':
        return True
    else:
        return False


def insertLetter(letter, position):
    if spaceIsFree(position):
        board[position] = letter
        return
    return


def checkForWin():
    if (board[1] == board[2] and board[1] == board[3] and board[1] != '__'):
        return True
    elif (board[4] == board[5] and board[4] == board[6] and board[4] != '__'):
        return True
    elif (board[7] == board[8] and board[7] == board[9] and board[7] != '__'):
        return True
    elif (board[1] == board[4] and board[1] == board[7] and board[1] != '__'):
        return True
    elif (board[2] == board[5] and board[2] == board[8] and board[2] != '__'):
        return True
    elif (board[3] == board[6] and board[3] == board[9] and board[3] != '__'):
        return True
    elif (board[1] == board[5] and board[1] == board[9] and board[1] != '__'):
        return True
    elif (board[7] == board[5] and board[7] == board[3] and board[7] != '__'):
        return True
    else:
        return False


def checkWhichMarkWon(mark):
    if board[1] == board[2] and board[1] == board[3] and board[1] == mark:
        return True
    elif (board[4] == board[5] and board[4] == board[6] and board[4] == mark):
        return True
    elif (board[7] == board[8] and board[7] == board[9] and board[7] == mark):
        return True
    elif (board[1] == board[4] and board[1] == board[7] and board[1] == mark):
        return True
    elif (board[2] == board[5] and board[2] == board[8] and board[2] == mark):
        return True
    elif (board[3] == board[6] and board[3] == board[9] and board[3] == mark):
        return True
    elif (board[1] == board[5] and board[1] == board[9] and board[1] == mark):
        return True
    elif (board[7] == board[5] and board[7] == board[3] and board[7] == mark):
        return True
    else:
        return False


def checkDraw():
    for key in board.keys():
        if (board[key] == '__'):
            return False
    return True


def compMove():
    bestScore = -800
    bestMove = 0
    for key in board.keys():
        if (board[key] == '__'):
            board[key] = bot1
            score = minimax(board, 0, False)
            board[key] = '__'
            if (score > bestScore):
                bestScore = score
                bestMove = key

    insertLetter(bot1, bestMove)
    return


def minimax(board, depth, isMaximizing):
    if (checkWhichMarkWon(bot1)):
        return 1
    elif (checkWhichMarkWon(player)):
        return -1
    elif (checkDraw()):
        return 0

    if (isMaximizing):
        bestScore = -800
        for key in board.keys():
            if (board[key] == '__'):
                board[key] = bot1
                score = minimax(board, depth + 1, False)
                board[key] = '__'
                if (score > bestScore):
                    bestScore = score
        return bestScore

    else:
        bestScore = 800
        for key in board.keys():
            if (board[key] == '__'):
                board[key] = player
                score = minimax(board, depth + 1, True)
                board[key] = '__'
                if (score < bestScore):
                    bestScore = score
        return bestScore


board = {1: '__', 2: '__', 3: '__',
         4: '__', 5: '__', 6: '__',
         7: '__', 8: '__', 9: '__'}

player = 'O'
bot1 = 'X'


storage = MemoryStorage()

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot, storage=storage)

win_draw = False

def board_zeroing_out():
    global board
    board = {1: '__', 2: '__', 3: '__',
         4: '__', 5: '__', 6: '__',
         7: '__', 8: '__', 9: '__'}

async def create_buttons():
    kb = InlineKeyboardMarkup(resize_keyboard=True)
    b1 = InlineKeyboardButton(f"{board[1]}", callback_data="1")
    b2 = InlineKeyboardButton(f"{board[2]}", callback_data="2")
    b3 = InlineKeyboardButton(f"{board[3]}", callback_data="3")
    b4 = InlineKeyboardButton(f"{board[4]}", callback_data="4")
    b5 = InlineKeyboardButton(f"{board[5]}", callback_data="5")
    b6 = InlineKeyboardButton(f"{board[6]}", callback_data="6")
    b7 = InlineKeyboardButton(f"{board[7]}", callback_data="7")
    b8 = InlineKeyboardButton(f"{board[8]}", callback_data="8")
    b9 = InlineKeyboardButton(f"{board[9]}", callback_data="9")
    kb.add(b1, b2, b3, b4, b5, b6, b7, b8, b9)
    return kb


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, "Hello, this is a bot with which you can play tic tac toe", reply_markup=button.kb)


@dp.message_handler()
async def start_the_game(message: types.Message, state: FSMContext):
    global win_draw
    if message.text == "Bot go first":
        compMove()
        win_draw = False
        await bot.send_message(message.from_user.id, "You play for 'O'", reply_markup=button.kb2)
        await bot.send_message(message.from_user.id, "Board", reply_markup=await create_buttons())
    elif message.text == "Go first":
        win_draw = False
        await bot.send_message(message.from_user.id, "You play for 'O'", reply_markup=button.kb2)
        await bot.send_message(message.from_user.id, "Board", reply_markup=await create_buttons())
    elif message.text == "Stop game":
        await bot.send_message(message.from_user.id, "Ок((", reply_markup=button.kb2)
    else:
        await bot.send_message(message.from_user.id, "Do you want play to game tic tac toe?, click on board")


@dp.callback_query_handler()
async def game(query: types.CallbackQuery):
    global win_draw
    if not win_draw:
        if spaceIsFree(int(query.data)):
            insertLetter("O", int(query.data))
            if checkWhichMarkWon("O"):
                win_draw = True
                await query.message.answer("You won!! (Have you played for 'O')", reply_markup=button.kb)
                board_zeroing_out()
            elif checkWhichMarkWon("X"):
                win_draw = True
                await query.message.answer("Bot won!! (Have bot played for 'X')", reply_markup=button.kb)
                board_zeroing_out()
            elif checkDraw():
                win_draw = True
                await query.message.answer("Draw!!", reply_markup=button.kb)
                board_zeroing_out()
            else:
                await query.message.edit_reply_markup(await create_buttons())
                compMove()
                if checkWhichMarkWon("O"):
                    win_draw = True
                    await query.message.edit_reply_markup(await create_buttons())
                    await query.message.answer("You won!! (Have you played for 'O')", reply_markup=button.kb)
                    board_zeroing_out()
                elif checkWhichMarkWon("X"):
                    win_draw = True
                    await query.message.edit_reply_markup(await create_buttons())
                    await query.message.answer("Bot won!! (Have bot played for 'X')", reply_markup=button.kb)
                    board_zeroing_out()
                elif checkDraw():
                    win_draw = True
                    await query.message.edit_reply_markup(await create_buttons())
                    await query.message.answer("Draw!!", reply_markup=button.kb)
                    board_zeroing_out()
                else:
                    await query.message.edit_reply_markup(await create_buttons())
        else:
            await query.message.answer("Space is not free!!!")

executor.start_polling(dp, skip_updates=True)
