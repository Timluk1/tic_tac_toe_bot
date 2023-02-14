from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, Dispatcher, StatesGroup
from aiogram import types
import button
from aiogram.utils import executor
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

global firstComputerMove
firstComputerMove = True

storage = MemoryStorage()

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot, storage=storage)


class FSMAdmin(StatesGroup):
    answer = State()
    answer2 = State()


@dp.message_handler(commands=["start"])
async def admin(message: types.Message):
    await bot.send_message(message.from_user.id, "Hello, this is a bot with which you can play tic tac toe", reply_markup=button.kb)


@dp.message_handler(state=None)
async def cm_start(message: types.Message, state: FSMContext):
    if message.text == "Bot go first":
        compMove()
        await bot.send_message(message.from_user.id, "The game board is numbered:\n1|2|3\n4|5|6\n7|8|9")
        await bot.send_message(message.from_user.id, "You play for the 'O'")
        await bot.send_message(message.from_user.id, 
                               board[1] + '|' + board[2] + '|' + board[3] + "\n" + board[4] + '|' + board[5] + '|' +
                               board[6] + "\n" + board[7] + '|' + board[8] + '|' + board[9])
        await bot.send_message(message.from_user.id, "Number on board please", reply_markup=button.kb2)
        await FSMAdmin.answer.set()
    elif message.text == "Go first":
        await bot.send_message(message.from_user.id, "The game board is numbered:\n1|2|3\n4|5|6\n7|8|9")
        await bot.send_message(message.from_user.id, "You play for the 'O'")
        await bot.send_message(message.from_user.id, "Number on board please", reply_markup=button.kb2)
        await FSMAdmin.answer2.set()
    else:
        await bot.send_message(message.from_user.id, "Do you want play to game tic tac toe?, click on board")

@dp.message_handler(state=FSMAdmin.answer2)
async def load_chapter2(message: types.Message, state: FSMContext):
    global board
    try:
        if message.text == "Stop game":
            await bot.send_message(message.from_user.id, "Ок(", reply_markup=button.kb)
            board = {1: '__', 2: '__', 3: '__',
                4: '__', 5: '__', 6: '__',
                7: '__', 8: '__', 9: '__'}
            await state.finish()
        elif spaceIsFree(int(message.text)):
            insertLetter(player, int(message.text))
            if checkWhichMarkWon("O"):
                await bot.send_message(message.from_user.id, "'O' win!!!", reply_markup=button.kb)
                await bot.send_message(message.from_user.id,
                                        board[1] + '|' + board[2] + '|' + board[3] + "\n" + board[4] + '|' + board[5] + '|' +
                                        board[6] + "\n" + board[7] + '|' + board[8] + '|' + board[9])
                board = {1: '__', 2: '__', 3: '__',
                    4: '__', 5: '__', 6: '__',
                    7: '__', 8: '__', 9: '__'}
                await state.finish()

            elif checkDraw():
                await bot.send_message(message.from_user.id, "Draw!!!", reply_markup=button.kb)
                await bot.send_message(message.from_user.id,
                                        board[1] + '|' + board[2] + '|' + board[3] + "\n" + board[4] + '|' + board[5] + '|' +
                                        board[6] + "\n" + board[7] + '|' + board[8] + '|' + board[9])
                board = {1: '__', 2: '__', 3: '__',
                4: '__', 5: '__', 6: '__',
                7: '__', 8: '__', 9: '__'}
                await state.finish()
            compMove()    
            if checkWhichMarkWon("X"):
                await bot.send_message(message.from_user.id, "'X' win!!!", reply_markup=button.kb)
                await bot.send_message(message.from_user.id,
                                        board[1] + '|' + board[2] + '|' + board[3] + "\n" + board[4] + '|' + board[5] + '|' +
                                        board[6] + "\n" + board[7] + '|' + board[8] + '|' + board[9])
                board = {1: '__', 2: '__', 3: '__',
                4: '__', 5: '__', 6: '__',
                7: '__', 8: '__', 9: '__'}
                await state.finish()

            elif checkDraw():
                await bot.send_message(message.from_user.id, "Draw!!!, reply_markup=button.kb")
                await bot.send_message(message.from_user.id,
                                        board[1] + '|' + board[2] + '|' + board[3] + "\n" + board[4] + '|' + board[5] + '|' +
                                        board[6] + "\n" + board[7] + '|' + board[8] + '|' + board[9])
                board = {1: '__', 2: '__', 3: '__',
                4: '__', 5: '__', 6: '__',
                7: '__', 8: '__', 9: '__'}
                await state.finish()
            else:
                await bot.send_message(message.from_user.id,
                                    board[1] + '|' + board[2] + '|' + board[3] + "\n" + board[4] + '|' + board[5] + '|' +
                                    board[6] + "\n" + board[7] + '|' + board[8] + '|' + board[9])
                await bot.send_message(message.from_user.id, "Number on board please")
        else:
            await bot.send_message(message.from_user.id, "Space is not free!!")
    except Exception:
        await bot.send_message(message.from_user.id, "It is not number(. Send number please")



@dp.message_handler(state=FSMAdmin.answer)
async def load_chapter(message: types.Message, state: FSMContext):
    global board
    try:
        if message.text == "Stop game":
            await bot.send_message(message.from_user.id, "Ок(", reply_markup=button.kb)
            board = {1: '__', 2: '__', 3: '__',
                4: '__', 5: '__', 6: '__',
                7: '__', 8: '__', 9: '__'}
            await state.finish()
        elif spaceIsFree(int(message.text)):
            insertLetter(player, int(message.text))
            if checkWhichMarkWon("O"):
                await bot.send_message(message.from_user.id, "'O' win!!!", reply_markup=button.kb)
                await bot.send_message(message.from_user.id,
                                    board[1] + '|' + board[2] + '|' + board[3] + "\n" + board[4] + '|' + board[5] + '|' +
                                    board[6] + "\n" + board[7] + '|' + board[8] + '|' + board[9])
                board = {1: '__', 2: '__', 3: '__',
                4: '__', 5: '__', 6: '__',
                7: '__', 8: '__', 9: '__'}
                await state.finish()

            elif checkDraw():
                await bot.send_message(message.from_user.id, "Draw!!!", reply_markup=button.kb)
                await bot.send_message(message.from_user.id,
                                    board[1] + '|' + board[2] + '|' + board[3] + "\n" + board[4] + '|' + board[5] + '|' +
                                    board[6] + "\n" + board[7] + '|' + board[8] + '|' + board[9])
                board = {1: '__', 2: '__', 3: '__',
                4: '__', 5: '__', 6: '__',
                7: '__', 8: '__', 9: '__'}
                await state.finish()
            compMove()    
            if checkWhichMarkWon("X"):
                await bot.send_message(message.from_user.id, "'X' win!!!", reply_markup=button.kb)
                await bot.send_message(message.from_user.id,
                                    board[1] + '|' + board[2] + '|' + board[3] + "\n" + board[4] + '|' + board[5] + '|' +
                                    board[6] + "\n" + board[7] + '|' + board[8] + '|' + board[9])
                board = {1: '__', 2: '__', 3: '__',
                4: '__', 5: '__', 6: '__',
                7: '__', 8: '__', 9: '__'}
                await state.finish()
            
            elif checkDraw():
                await bot.send_message(message.from_user.id, "Draw!!!", reply_markup=button.kb)
                await bot.send_message(message.from_user.id,
                                    board[1] + '|' + board[2] + '|' + board[3] + "\n" + board[4] + '|' + board[5] + '|' +
                                    board[6] + "\n" + board[7] + '|' + board[8] + '|' + board[9])
                board = {1: '__', 2: '__', 3: '__',
                4: '__', 5: '__', 6: '__',
                7: '__', 8: '__', 9: '__'}
                await state.finish()

            else:
                await bot.send_message(message.from_user.id,
                                    board[1] + '|' + board[2] + '|' + board[3] + "\n" + board[4] + '|' + board[5] + '|' +
                                    board[6] + "\n" + board[7] + '|' + board[8] + '|' + board[9])
                await bot.send_message(message.from_user.id, "Number on board please")
        else:
            await bot.send_message(message.from_user.id, "Space is not free!!")
    except Exception:
        await bot.send_message(message.from_user.id, "It is not number(. Send number please")
    


executor.start_polling(dp, skip_updates=True)
