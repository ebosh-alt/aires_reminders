import logging
import re

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from data.config import config

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("on"))
async def on(message: Message):
    config.enabled = True
    config.save_config()
    logger.info(config)
    await message.answer("Параметр обновлен")


@router.message(Command("off"))
async def off(message: Message):
    config.enabled = False
    config.save_config()
    logger.info(config)
    await message.answer("Параметр обновлен")


def is_valid_time_format(time_str: str) -> bool:
    """
    Проверяет, соответствует ли строка формату времени ЧЧ:ММ.

    Args:
        time_str (str): Строка с временем.

    Returns:
        bool: True, если строка соответствует формату ЧЧ:ММ, иначе False.
    """
    # Регулярное выражение для формата ЧЧ:ММ, где ЧЧ от 00 до 23 и ММ от 00 до 59
    time_pattern = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")
    return bool(time_pattern.match(time_str))


@router.message(Command("set_start"))
async def set_start(message: Message):
    data = message.text.split(" ")
    if len(data) == 1:
        return await message.answer("Неверный формат времени. Пример: /set_start 02:00")
    times = data[1].strip()
    if is_valid_time_format(times):
        config.start_time = times
        config.save_config()
        logger.info(config)
        await message.answer("Параметр обновлен")
    else:
        await message.answer("Неверный формат времени. Пример: /set_start 02:00")


@router.message(Command("set_delay"))
async def set_delay(message: Message):
    data = message.text.split(" ")
    if len(data) == 1:
        return await message.answer("Неверный формат времени. Пример: /set_start 02:00")
    delay = data[1].strip()
    if delay.isdigit():
        config.delay = int(delay)
        config.save_config()
        logger.info(config)
        await message.answer("Параметр обновлен")
    else:
        await message.answer("Неверное значение задержки. Пример: /set_delay 5")


def is_valid_email(email: str) -> bool:
    """
    Проверяет, является ли строка корректным адресом электронной почты.

    Args:
        email (str): Строка с адресом электронной почты.

    Returns:
        bool: True, если строка соответствует формату email, иначе False.
    """
    # Регулярное выражение для валидации email-адреса
    email_pattern = re.compile(
        r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    )
    return bool(email_pattern.match(email))


@router.message(Command("set_emails"))
async def set_emails(message: Message):
    data = message.text.split(" ")
    if len(data) == 1:
        return await message.answer("Неверный формат времени. Пример: /set_start 02:00")
    emails = data[1:]
    err = False
    for email in emails:
        if not is_valid_email(email):
            err = True
    if not err:
        config.emails = emails
        config.save_config()
        logger.info(config)
        await message.answer("Параметр обновлен")
    else:
        await message.answer("Неверные адреса электронной почты. Пример: /set_emails 1@example.com 2@example.com")


commands_router = router
