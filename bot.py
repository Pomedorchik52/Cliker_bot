import asyncio
import logging
from os import getenv
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

TOKEN = getenv("BOT_TOKEN")
if not TOKEN:
    TOKEN = "Ваш токен"

bot = Bot(token=TOKEN)
dp = Dispatcher()

users = {}

main_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Старт", callback_data="start")],
        [InlineKeyboardButton(text="Помощь", callback_data="help")],
        [InlineKeyboardButton(text="Статистика", callback_data="stats")],
        [InlineKeyboardButton(text="Играть", callback_data="game")],
    ]
)

game_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="click")],
        [KeyboardButton(text="В главное меню")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def start_command(message: Message):
    user_id = message.from_user.id
    if user_id not in users:
        users[user_id] = {"level": 1, "exp": 0, "money": 0, "clicks": 0}

    username = message.from_user.username or message.from_user.first_name
    await message.answer(
        f"🍅 Привет, {username}! Добро пожаловать в «Тыкни помидор»!",
        reply_markup=main_kb
    )

@dp.callback_query(F.data == "start")
async def inline_start(callback: CallbackQuery):
    username = callback.from_user.username or callback.from_user.first_name
    await callback.message.answer(f"Привет, {username}!")
    await callback.answer()

@dp.callback_query(F.data == "help")
async def inline_help(callback: CallbackQuery):
    await callback.message.answer(
        "Вот что я умею:\n"
        "/start - Запуск бота\n"
        "Играть - начать игру\n"
        "Статистика - показать твою статистику\n"
    )
    await callback.answer()

@dp.callback_query(F.data == "stats")
async def inline_stats(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in users:
        await callback.message.answer("Сначала введи /start!")
        await callback.answer()
        return

    stats = users[user_id]
    await callback.message.answer(
        f"📊 Ваша статистика:\n"
        f"Уровень: {stats['level']}lvl\n"
        f"Опыт: {stats['exp']}exp\n"
        f"Деньги: {stats['money']}\n"
        f"Клики: {stats['clicks']}шт"
    )
    await callback.answer()

@dp.callback_query(F.data == "game")
async def inline_game(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in users:
        users[user_id] = {"level": 1, "exp": 0, "money": 0, "clicks": 0}

    await callback.message.answer(
        "Начинаем игру! Нажимай на помидоры 🍅",
        reply_markup=game_kb
    )
    await callback.answer()

@dp.message(F.text == "click")
async def click_game(message: Message):
    user_id = message.from_user.id
    if user_id not in users:
        users[user_id] = {"level": 1, "exp": 0, "money": 0, "clicks": 0}

    users[user_id]["clicks"] += 1
    users[user_id]["exp"] += 1
    users[user_id]["money"] += 1

    if users[user_id]["exp"] >= users[user_id]["level"] * 50:
        users[user_id]["level"] += 1
        await message.answer(f"🎉 Поздравляем! Вы достигли уровня {users[user_id]['level']}!")

    await message.answer(f"Ты кликнул! Клики: {users[user_id]['clicks']}")

@dp.message(F.text == "В главное меню")
async def back_to_menu(message: Message):
    await message.answer("Возврат в главное меню:", reply_markup=main_kb)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
