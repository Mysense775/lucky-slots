#!/usr/bin/env python3
"""
🎰 Lucky Slots - Mini App Casino Bot
Telegram Mini App with slot machine game
"""

import asyncio
import logging
import json
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command

# Logging
logging.basicConfig(level=logging.INFO)

# Bot token (create via @BotFather)
BOT_TOKEN = "8500469192:AAE-fnqfbRchyOTvNh0GpqbPvpzUsUg6OTc"

# WebApp URL (GitHub Pages or your server)
WEBAPP_URL = "https://mysense775.github.io/lucky-slots/index.html?v=3"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Start command with WebApp button"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🎰 ИГРАТЬ В СЛОТЫ", 
            web_app=WebAppInfo(url=WEBAPP_URL)
        )],
        [InlineKeyboardButton(
            text="💰 Пополнить баланс", 
            callback_data="deposit"
        )],
        [InlineKeyboardButton(
            text="📊 Таблица лидеров", 
            callback_data="leaderboard"
        )]
    ])
    
    await message.answer(
        "🎰 <b>Добро пожаловать в Lucky Slots!</b>\n\n"
        "💎 Лучший слот-машина в Telegram\n"
        "⚡ Мгновенные выплаты\n"
        "🎁 Бонус при регистрации: 1000 💎\n\n"
        "Нажми кнопку ниже чтобы начать! 👇",
        reply_markup=keyboard,
        parse_mode='HTML'
    )

@dp.message(Command("play"))
async def cmd_play(message: types.Message):
    """Direct play command"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🎰 ЗАПУСТИТЬ ИГРУ", 
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ])
    
    await message.answer(
        "🎰 <b>Готов к игре?</b>\n\n"
        "Нажми кнопку чтобы открыть слот-машину!",
        reply_markup=keyboard,
        parse_mode='HTML'
    )

@dp.message(Command("balance"))
async def cmd_balance(message: types.Message):
    """Check balance"""
    # TODO: Get balance from database
    await message.answer(
        "💎 <b>Ваш баланс:</b> 1000 💎\n\n"
        "Для пополнения используйте /deposit",
        parse_mode='HTML'
    )

@dp.message(lambda message: message.web_app_data is not None)
async def webapp_data(message: types.Message):
    """Handle data from WebApp"""
    try:
        data = json.loads(message.web_app_data.data)
        action = data.get('action')
        
        if action == 'game_end':
            balance = data.get('balance', 0)
            await message.answer(
                f"🎰 <b>Игра завершена!</b>\n\n"
                f"💎 Итоговый баланс: {balance}",
                parse_mode='HTML'
            )
            
    except Exception as e:
        logging.error(f"WebApp data error: {e}")

@dp.callback_query(lambda c: c.data == "deposit")
async def deposit_callback(callback: types.CallbackQuery):
    """Handle deposit button"""
    await callback.answer("💰 Открываю меню пополнения...")
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="100 💎 - 1⭐", callback_data="buy_100"),
            InlineKeyboardButton(text="500 💎 - 5⭐", callback_data="buy_500")
        ],
        [
            InlineKeyboardButton(text="1000 💎 - 9⭐", callback_data="buy_1000"),
            InlineKeyboardButton(text="5000 💎 - 45⭐", callback_data="buy_5000")
        ],
        [InlineKeyboardButton(text="🎰 Играть", web_app=WebAppInfo(url=WEBAPP_URL))]
    ])
    
    await callback.message.answer(
        "💎 <b>Пополнение баланса</b>\n\n"
        "Выберите пакет кристаллов:\n"
        "• 100 💎 = 1 Telegram Star\n"
        "• 500 💎 = 5 Stars (-10%)\n"
        "• 1000 💎 = 9 Stars (-10%)\n"
        "• 5000 💎 = 45 Stars (-10%)\n\n"
        "⚡ Мгновенное зачисление!",
        reply_markup=keyboard,
        parse_mode='HTML'
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
