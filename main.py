from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
import asyncio
from routrs import router

TOKEN = ""
dp = Dispatcher()


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_routers(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
