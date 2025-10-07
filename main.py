from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from time import sleep
from art import tprint
import tqdm
from colorama import init, Fore, Style
import os
from dotenv import load_dotenv, set_key
import webbrowser
from datetime import datetime

init(autoreset=True)
load_dotenv()

def shutdown():
    print("Завершаю cmd процесс...")
    sleep(2)
    print("чао!")
    sleep(1)

def auth_input():
    mospolytech_login = os.getenv("ENV_mospolytech_login")
    mospolytech_password = os.getenv("ENV_mospolytech_password")

    if not mospolytech_login or not mospolytech_password:
        print(Fore.RED + 'Нет данных! Заполните поля')
        mospolytech_login = input('Введите логин от ЛК политеха >>> ')
        mospolytech_password = input('Введите пароль от ЛК политеха (начинается со Stud) >>> ')
        set_key(".env", "ENV_mospolytech_login", mospolytech_login)
        set_key(".env", "ENV_mospolytech_password", mospolytech_password)
    
    return mospolytech_login, mospolytech_password

def login_lk(page, login, password):
    page.goto("https://e.mospolytech.ru/#/schedule/current", wait_until="networkidle")

    page.fill('input[placeholder="Введите логин"]', login)
    page.fill('input[placeholder="Введите пароль"]', password)

    page.locator('button.submit-button').first.click()

    try:
        page.wait_for_selector('a.sc-djarn2-0.csPclf', timeout=15000)
        print(Fore.GREEN + 'Успешный вход!')
    except Exception as error:
        print(Fore.RED + f"Auth failed with error: {error}")

def parse_calendar(page):
    current_datetime = datetime.now()
    current_index_date = current_datetime.weekday()

    weekday = {
        0: 'Понедельник',
        1: 'Вторник',
        2: 'Среда',
        3: 'Четверг',
        4: 'Пятница',
        5: 'Суббота'
    }

    print(f"Сегодня {current_datetime.strftime('%d.%m.%Y')} {weekday.get(current_index_date, None)}")

    page.goto("https://e.mospolytech.ru/#/schedule/current", wait_until="networkidle")
    print("\nПарсим данные")
    for _ in tqdm.tqdm(range(10)):
        sleep(0.35)

    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    array_links = []

    day_divs = soup.find_all("div", class_="sc-1j9n86g-0 jxiZdc calendar-wrapper")
    if not day_divs or len(day_divs) < 6:
        print(Fore.RED + "Не удалось найти 6 div")
        return []

    current_day_div = day_divs[current_index_date]

    for span in current_day_div.find_all("span", string=lambda s: s and "(Лекция)" in s):
        a_tag = span.find_previous("a", href=True)
        if a_tag and a_tag["href"] != "https://online.mospolytech.ru/":
            array_links.append(a_tag["href"])

    if not array_links:
        print(Fore.RED + "Я не вижу ни одной ссылки :(")
        return None

    return array_links

def open_links(array_links):
    if array_links and len(array_links) > 0:
        print("Подключаюсь к лекциям...")
        try:
            webbrowser.open_new('https://google.com')
            sleep(3)
            for link in array_links:
                webbrowser.open_new_tab(link)
                sleep(5)
        except Exception as error:
            print(Fore.RED + f'Error! {error}')
    shutdown()

def app():
    tprint("EZ LECTURE")
    mospolytech_login, mospolytech_password = auth_input()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()
        page.goto("https://e.mospolytech.ru/#/schedule/current", wait_until="networkidle")
            
        login_lk(page, mospolytech_login, mospolytech_password)
        array_links = parse_calendar(page)
        browser.close()
        open_links(array_links)

if __name__ == "__main__":
    app()