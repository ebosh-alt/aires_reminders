import json
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any

from aiogram import Dispatcher, Bot
from environs import Env

env = Env()
env.read_env()

bot_token = env('BOT_TOKEN')
aires_api_key = env('AIRES_API_KEY')
ADMINS = [int(admin_id) for admin_id in env('ADMINS').split()]
dp = Dispatcher()
bot = Bot(bot_token)

CONFIG_FILE = "data/config.json"

logger = logging.getLogger(__name__)
DIVISION_ID = "14"
REQUIRED_FIELDS = {"3644", "3657"}  # Пример: поля с id 3643, 3644 и 3657
REQUIRED_FIELDS_DEALS = {"3770", "3850", "3851"}


@dataclass
class Config:
    """Класс для работы с конфигурацией."""
    enabled: bool = True
    start_time: str = "02:00"
    delay: int = 6
    emails: List[str] = field(default_factory=list)
    admins: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Загружает конфигурацию из файла при инициализации экземпляра."""
        config_data = self.load_config()
        if config_data:  # Загружаем данные, если файл существует и не пустой
            self.set_config(config_data)

    def set_config(self, config_data: Dict[str, Any]) -> None:
        """Обновляет значения конфигурации из словаря.
        :param config_data: (Dict[str, Any]) Словарь с параметрами конфигурации:
                - enabled (bool): Включение/отключение работы, по умолчанию True.
                - start_time (str): Время старта в формате 'HH:MM', по умолчанию '02:00'.
                - delay (int): Задержка в часах перед отключением лидов, по умолчанию 6.
                - emails (List[str]): Список e-mail для уведомлений, по умолчанию пустой.
        """
        self.enabled = config_data.get('enabled', self.enabled)
        self.start_time = config_data.get('start_time', self.start_time)
        self.delay = config_data.get('delay', self.delay)
        self.emails = config_data.get('emails', self.emails)

    def save_config(self) -> None:
        """Сохраняет обновленные параметры в конфигурационный файл."""
        config_json = {
            "enabled": self.enabled,
            "start_time": self.start_time,
            "delay": self.delay,
            "emails": self.emails,
            "admins": [686171972]
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config_json, f, indent=4)

    @staticmethod
    def load_config() -> dict | None:
        """Загружает параметры конфигурации из файла, если файл существует."""
        try:
            with open(CONFIG_FILE, 'r') as f:
                config_json = json.load(f)
                return config_json
        except FileNotFoundError:
            logger.info(f"Файл конфигурации '{CONFIG_FILE}' не найден. Используются значения по умолчанию.")
            return None
        except json.JSONDecodeError:
            logger.info("Ошибка чтения конфигурационного файла. Проверьте его формат.")
            return None


config = Config()
sender = "bvvrus@gmail.com"
# sender = "isakovn2005@gmail.com"
password = "zqtl ujdy hzyt tymi"
# password = "ppca spzv qseg jhen"
