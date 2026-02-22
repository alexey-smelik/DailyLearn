"""tg-tool entry point: FastAPI HTTP server + aiogram bot polling."""

import asyncio
import logging

import uvicorn
from aiogram import Bot, Dispatcher
from fastapi import FastAPI

from app.api.router import router as api_router
from app.bot.router import router as bot_router
from app.config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


def create_app(bot: Bot) -> FastAPI:
    app = FastAPI(title="tg-tool", version="0.1.0")
    app.state.bot = bot
    app.include_router(api_router)
    return app


async def main() -> None:
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    dp.include_router(bot_router)

    app = create_app(bot)
    config = uvicorn.Config(app, host=settings.host, port=settings.port, log_level="info")
    server = uvicorn.Server(config)

    await asyncio.gather(
        server.serve(),
        dp.start_polling(bot, allowed_updates=["message", "callback_query"]),
    )


if __name__ == "__main__":
    asyncio.run(main())
