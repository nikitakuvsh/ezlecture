import os
import platform
import subprocess
import sys

def main():
    system = platform.system()

    if system == "Windows":
        activate_path = r"venv\Scripts\activate"
        python_path = r"venv\Scripts\python.exe"
    else:
        activate_path = "source venv/bin/activate"
        python_path = "venv/bin/python"

    if not os.path.exists("venv"):
        print("❌ Виртуальное окружение не найдено. Сначала запусти setup.py.")
        sys.exit(1)

    # Проверяем, существует ли main.py
    if not os.path.exists("main.py"):
        print("❌ Исполняемый файл не найден")
        sys.exit(1)

    # На Windows активировать среду напрямую нельзя, просто используем python из venv
    result = subprocess.run([python_path, "main.py"], shell=True)

    if result.returncode == 0:
        print("\n🎉 Скрипт успешно выполнен!")
    else:
        print("\n❌ Ошибка при запуске main.py")

if __name__ == "__main__":
    main()
