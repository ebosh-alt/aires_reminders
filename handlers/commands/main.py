import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from data.config import config
from filters.Filters import IsAdmin
from services.validate import is_valid_time_format, is_valid_email

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("on"), IsAdmin())
async def on(message: Message):
    config.enabled = True
    config.save_config()
    logger.info(config)
    await message.answer("Параметр обновлен")


@router.message(Command("off"), IsAdmin())
async def off(message: Message):
    config.enabled = False
    config.save_config()
    logger.info(config)
    await message.answer("Параметр обновлен")


@router.message(Command("set_start"), IsAdmin())
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


@router.message(Command("set_delay"), IsAdmin())
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


@router.message(Command("set_emails"), IsAdmin())
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
