import asyncio
import datetime
import logging
import time

import requests
import schedule

from data.config import Config, sender, password, aires_api_key
from services.Intrum.Client import ClientIntrum
from services.emails import MailService

logger = logging.getLogger(__name__)


class Schedule:
    def __init__(self):
        self.api_key = aires_api_key
        self.intrum = ClientIntrum(self.api_key)
        self.script_path = '../php_app/change_worker.php'
        self.url = "http://php_app:80/change_worker.php"

    async def work(self):
        users = await self.intrum.get_users()
        expired_users = await self.intrum.get_users_expired()
        deals = await self.intrum.get_deals(users)
        expired_deals = await self.intrum.get_deals(expired_users)
        await self.check_user(deals, "Лиды Отключены")
        await self.check_user(expired_deals, "Лиды Включены")

    async def check_user(self, deals, value_field):
        try:
            ms = MailService(sender=sender, password=password)
            config = Config()
            delay = datetime.timedelta(hours=config.delay)
            now = datetime.datetime.now()
            data = {}
            send_message = "Id пользователей: "
            send = False
            for deal in deals:
                if deal:
                    reminder = await self.intrum.get_reminder(deal.fields["3770"].value)
                    if reminder:
                        if now - delay > reminder.dtend:
                            data[deal.employee_id] = True
                        else:
                            data[deal.employee_id] = False
            for user_id in data:
                if user_id == "952":
                    if value_field == "Лиды Отключены":
                        if data[user_id]:
                            status = self.change_worker(user_id=str(user_id), value=value_field)
                            logger.info(status)
                            if status:
                                send = True
                                send_message += f"{user_id}, "
                                logger.info(f"Пользователь изменен(Лиды Отключены): {user_id}")
                        else:
                            if not data[user_id]:
                                status = self.change_worker(user_id=str(user_id), value=value_field)
                                if status:
                                    send = True
                                    send_message += f"{user_id}\n"
                                    logger.info(f"Пользователь изменен(Лиды Включены): {user_id}")

            if send:
                try:
                    if value_field == "Лиды Включены":
                        ms.send("Восстановили сделки", send_message[0:-2])
                    else:
                        ms.send("Пропущено уведомление", send_message[0:-2])
                    logger.info(f"Email успешно отправлена: {send_message}")
                except Exception as e:
                    logger.info(f"Не получилось отправить Email: {e}")
        except Exception as e:
            logger.info(f"Ошибка при обращении к серверу: {e}")

    def change_worker(self, user_id: str = "1125", value: str = "Лиды Отключены"):
        try:
            response = requests.post(self.url, json={"api_key": self.api_key, "user_id": user_id, "value_field": value})
            logger.info(response)
            if response.status_code == 200:
                data = response.json()
                logger.info(data)
                if data["status"] == "success":
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            logger.info(e)
            return False

    def run_async_work(self):
        asyncio.run(self.work())

    def schedule_check(self):
        config = Config()
        """Перенастраивает планировщик на основе текущей конфигурации."""
        schedule.clear()  # Очистить предыдущее расписание
        schedule.every().day.at(config.start_time).do(self.run_async_work)

    def run(self):
        last_check_time = None
        while True:
            config = Config()
            time.sleep(10 * 60)
            if config.enabled:
                schedule.run_pending()
                current_check_time = config.start_time
                if current_check_time != last_check_time:
                    logger.info(f"Обнаружено новое время запуска: {current_check_time}. Обновление расписания...")
                    self.schedule_check()
                    last_check_time = current_check_time

