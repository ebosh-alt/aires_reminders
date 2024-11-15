import json

import requests

# URL для отправки запроса
url = "http://aires.astoria-tula.ru/sharedapi/worker/update"

# Чтение входных данных (вместо 'php://input' используем sys.stdin для получения JSON данных)
# import sys
# input_data = sys.stdin.read()
# data = json.loads(input_data)

# Извлечение параметров
# apikey = data.get("api_key")  # Первый параметр
# user_id = data.get("user_id")  # Второй параметр
# value_field = data.get("value_field")  # Третий параметр

# Параметры для отправки
# params = [

# ]

# Данные для POST-запроса
post_data = {
    'apikey': "21d1c8300ca07c06bf8f3aac3c16c275",
    'params[0][id]': "1125",
    'params[0][fields][0][id]': "3657",
    'params[0][fields][0][value]': "Лиды Включены",

}

# Отправка POST-запроса
response = requests.post(url, data=post_data)

# Обработка ответа
result = response.json()

# Вывод результата в формате JSON
print(json.dumps(result, ensure_ascii=False, indent=4))
