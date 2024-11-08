import asyncio
import logging
from contextlib import suppress

from aiogram.types import BotCommand

from data.config import bot
from services.Intrum.Client import ClientIntrum
from services.scheduler import Schedule

logger = logging.getLogger(__name__)


async def set_commands():
    await bot.set_my_commands(commands=[BotCommand(command="on", description="включить процесс"),
                                        BotCommand(command="off", description="выключить процесс"),
                                        BotCommand(command="set_start",
                                                   description="установка времени начала проверки обработки лидов сотрудниками"),
                                        BotCommand(command="set_delay", description="время задержки обработки"),
                                        BotCommand(command="set_emails", description="установка email-ов для отправки"),
                                        ])


async def main() -> None:
    # logger.info(rm)
    # scheduler_process = Process(target=Schedule().run)
    # scheduler_process.start()
    # await set_commands()
    # for router in routers:
    #     dp.include_router(router)
    # dp.update.middleware(middleware.Logging())
    # await dp.start_polling(bot)
    # await Schedule().work()

    # client = ClientIntrum("21d1c8300ca07c06bf8f3aac3c16c275")
    scheduler = Schedule()
    await scheduler.work()
    # await client.change_user()
    # for worker in users:
    #     deals = await client.get_deal()
    # for deal in deals:
    #     logger.info(deal.model_dump_json(indent=4))
    # logger.info(reminder)
    # deals = await client.get_deals(workers)
    # reminders = []
    # for deal in deals:
    #     rm = await client.get_missed_reminder(deal.employee_id, deal.fields['3770'].value)
    #     logger.info(f"{deal.employee_id}, {deal.fields['3770'].value}")
    #     logger.info(rm)
    # logger.info(len(deals))
    # logger.info(deals)
    # rm = await client.get_reminders(104898)

    # Пример основного процесса, выполняющего свои задачи
    # for i in range(5):
    #     logger.info(f"Основной процесс выполняет задачу {i + 1}")
    #     time.sleep(10)
    # Остановка процесса планировщика по завершении работы основного процесса
    # scheduler_process.terminate()
    # scheduler_process.join()
    # logger.info("Планировщик завершен.")
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        # filename="log.logging",
        format=u'%(filename)s:%(lineno)d #%(levelname)-3s [%(asctime)s] - %(message)s',
        filemode="w",
        encoding='utf-8')

    with suppress(KeyboardInterrupt):
        asyncio.run(main())
