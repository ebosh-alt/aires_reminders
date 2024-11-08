import subprocess

# Путь к вашему PHP-скрипту
php_script = 'test.php'

# Выполнение PHP-скрипта через командную строку
def run_php_script(script_path):
    try:
        # Запуск PHP-скрипта
        result = subprocess.run(['php', script_path, ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Проверка наличия ошибок
        if result.returncode != 0:
            print(f"Ошибка при выполнении скрипта: {result.stderr}")
        else:
            print("Результат выполнения скрипта:")
            print(result.stdout)  # Вывод результата выполнения PHP-скрипта

    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Запуск PHP-скрипта
run_php_script(php_script)
