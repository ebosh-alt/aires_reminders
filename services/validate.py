import re


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
