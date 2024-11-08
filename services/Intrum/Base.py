import json
import logging

import aiohttp

from entities.models import User, Field

logger = logging.getLogger(__name__)


class BaseApi:
    def __init__(self, token):
        self.__token = token

    def _get_auth(self):
        auth = {
            "apikey": self.__token,
        }
        logger.info("Successfully get auth")
        return auth

    async def _post(self, url: str, additional_params: dict | list[dict]):
        params = self._get_auth()
        if additional_params:
            params.update(additional_params)

        async with aiohttp.ClientSession() as session:
            response = await session.post(url=url, data=params)
            if response.status == 200:
                logger.info(f"Successfully response {url}, status: {response.status}")
            else:
                logger.info(f"Error response {url}, status: {response.status}")
            data = await response.json()
            await session.close()
        return data

    async def _get(self, url: str, additional_params: dict | list[dict] = None):
        # Получаем авторизационные параметры
        params = self._get_auth()
        # Обновляем параметры, если переданы дополнительные
        if additional_params:
            params.update(additional_params)

        async with aiohttp.ClientSession() as session:
            # Выполняем GET-запрос
            response = await session.get(url=url, params=json.dumps(params))
            # Проверяем статус ответа
            if response.status == 200:
                logger.info(f"Successfully get response from {url}, status: {response.status}")
            else:
                logger.info(f"Error in response from {url}, status: {response.status}")

            # Читаем данные JSON из ответа
            data = await response.json()

            await session.close()

        return data
