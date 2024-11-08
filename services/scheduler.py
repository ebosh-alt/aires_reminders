import asyncio
import datetime
import logging
import subprocess
import time

import schedule

from data.config import Config, sender, password
from services.Intrum.Client import ClientIntrum
from services.emails import MailService

logger = logging.getLogger(__name__)


class Schedule:
    def __init__(self):
        self.api_key = "21d1c8300ca07c06bf8f3aac3c16c275"
        self.intrum = ClientIntrum(self.api_key)  # 21d1c8300ca07c06bf8f3aac3c16c275
        self.script_path = './change_worker.php'  # Путь к скрипту

    def schedule_check(self):
        config = Config()
        """Перенастраивает планировщик на основе текущей конфигурации."""
        schedule.clear()  # Очистить предыдущее расписание
        schedule.every().day.at(config.start_time).do(self.run_async_work)
        logger.info(f"Проверка лидов запланирована на {config.start_time} каждый день.")

    async def work(self):
        users = await self.intrum.get_users()
        logger.info(users)
        expired_users = await self.intrum.get_users_expired()
        deals = await self.intrum.get_deals(users)
        logger.info(deals)
        expired_deals = await self.intrum.get_deals(expired_users)
        await self.check_user(deals, "Лиды Отключены")
        await self.check_user(expired_deals, "Лиды Включены")

    async def check_user(self, deals, value_field):
        ms = MailService(sender=sender, password=password)
        config = Config()
        delay = datetime.timedelta(hours=config.delay)
        now = datetime.datetime.now()
        data = {
        }
        send_message = "Id пользователей: "
        send = False
        for deal in deals:
            if deal:
                reminder = await self.intrum.get_reminder(deal.fields["3770"].value)
                if deal.employee_id == "2":
                    logger.info(reminder)
                if reminder:
                    if now - delay > reminder.dtend:
                        data[deal.employee_id] = True
                    else:
                        data[deal.employee_id] = False
        for user_id in data:
            if value_field == "Лиды Отключены":
                if data[user_id]:
                    send = True
                    send_message += f"{user_id}, "
                    # self.change_worker(user_id=str(user_id), value="Лиды Включены")
                    self.change_worker(value=value_field)
                    logger.info(f"Пользователь изменен: {user_id}")
            else:
                if not data[user_id]:
                    send = True
                    send_message += f"{user_id}\n"
                    # self.change_worker(user_id=str(user_id), value="Лиды Включены")
                    self.change_worker(value=value_field)
                    logger.info(f"Пользователь изменен: {user_id}")

        if send:
            logger.info(send_message)
            if value_field == "Лиды Включены":
                ms.send("Восстановили сделки", send_message[0:-2])
            else:
                ms.send("Пропущено уведомление", send_message[0:-2])

    def change_worker(self, user_id: str = "1125", value: str = "Лиды Отключены"):
        try:
            result = subprocess.run(['php', self.script_path, self.api_key, user_id, value], stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                return True
            else:
                return False
        except Exception as e:
            logger.info(e)
            return False

    def run_async_work(self):
        asyncio.run(self.work())

    def run(self):
        last_check_time = None
        while True:
            config = Config()
            schedule.run_pending()
            time.sleep(60 + 10)
            # Проверка на обновление конфигурации каждые 10 минут
            current_check_time = config.start_time
            if current_check_time != last_check_time:
                # Перезагрузить расписание, если время запуска изменилось
                print(f"Обнаружено новое время запуска: {current_check_time}. Обновление расписания...")
                self.schedule_check()
                last_check_time = current_check_time
