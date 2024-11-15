import asyncio
import logging
from contextlib import suppress
from multiprocessing import Process

from aiogram.types import BotCommand

from data.config import bot, dp
from handlers import routers
from services import middleware
from services.scheduler import Schedule

logger = logging.getLogger(__name__)


async def set_commands():
    await bot.set_my_commands(commands=[BotCommand(command="on", description="включить процесс"),
                                        BotCommand(command="off", description="выключить процесс"),
                                        BotCommand(command="set_start",
                                                   description="установка времени начала проверки обработки лидов сотрудниками(09:30)"),
                                        BotCommand(command="set_delay", description="время задержки обработки в часах)"),
                                        BotCommand(command="set_emails", description="установка email-ов для отправки(через пробел)"),
                                        ])


async def main() -> None:
    # Schedule().change_worker(value="Лиды Включены")
    scheduler_process = Process(target=Schedule().run)
    scheduler_process.start()
    # await set_commands()
    # for router in routers:
    #     dp.include_router(router)
    # dp.update.middleware(middleware.Logging())
    # await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        # filename="log.logging",
        format=u'%(filename)s:%(lineno)d #%(levelname)-3s [%(asctime)s] - %(message)s',
        filemode="w",
        encoding='utf-8')

    with suppress(KeyboardInterrupt):
        asyncio.run(main())
