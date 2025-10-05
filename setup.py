import os
import subprocess
import sys
import platform
from time import sleep

def run_command(command, shell=True):
    print(f"\n⚙️ {command}")
    result = subprocess.run(command, shell=shell)
    if result.returncode != 0:
        print(f"❌ Ошибка при выполнении: {command}")
        sys.exit(1)

def main():
    print("🔧 Установка окружения...\n")

    run_command(f"{sys.executable} -m venv venv")

    if platform.system() == "Windows":
        activate_cmd = r"venv\Scripts\activate"
    else:
        activate_cmd = "source venv/bin/activate"

    print("✅ Виртуальное окружение создано.")

    requirements_file = "requirements.txt"
    if not os.path.exists(requirements_file):
        with open(requirements_file, "w", encoding="utf-8") as f:
            f.write("playwright\nbeautifulsoup4\n")
        print("📄 Файл requirements.txt создан автоматически.")

    pip_path = os.path.join("venv", "Scripts", "pip") if platform.system() == "Windows" else "venv/bin/pip"
    run_command(f"{pip_path} install -r requirements.txt")

    python_path = os.path.join("venv", "Scripts", "python") if platform.system() == "Windows" else "venv/bin/python"
    run_command(f"{python_path} -m playwright install")

    print("\n🎉 УСТАНОВКА ПРОШЛА УСПЕШНО")
    run_command("python main.py")

if __name__ == "__main__":
    main()
