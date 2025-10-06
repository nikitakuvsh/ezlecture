from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from time import sleep
from art import tprint
import tqdm
from colorama import init
init()
from colorama import Fore, Back, Style
import os
from dotenv import load_dotenv, set_key
import webbrowser
from datetime import datetime

load_dotenv()

def auth_and_parse():
    tprint("EZ LECTURE")
    mospolytech_login = os.getenv("ENV_mospolytech_login")
    mospolytech_password = os.getenv("ENV_mospolytech_password")
    if not mospolytech_login and not mospolytech_password:
        print(Fore.RED + 'No data! Please fill in the fields.' + Style.RESET_ALL)
        mospolytech_login = input('Enter your login (lk) >>> ')
        mospolytech_password = input('Enter your password (lk) beginning with "Stud" >>> ')
        set_key(".env", "ENV_mospolytech_login", mospolytech_login)
        set_key(".env", "ENV_mospolytech_password", mospolytech_password)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()
        page.goto("https://e.mospolytech.ru/#/schedule/current", wait_until="networkidle")

        page.wait_for_selector('input[placeholder="Введите логин"]')
        page.wait_for_selector('input[placeholder="Введите пароль"]')

        page.fill('input[placeholder="Введите логин"]', mospolytech_login)
        page.fill('input[placeholder="Введите пароль"]', mospolytech_password)

        page.locator('button.submit-button').first.click()

        try:
            page.wait_for_selector('a.sc-djarn2-0.csPclf', timeout=15000)
            print(Fore.GREEN + 'Succes auth!' + Style.RESET_ALL)

            current_datetime = datetime.now()
            current_datetime_day = str(current_datetime.day)
            current_datetime_month = str(current_datetime.month)
            current_datetime_year = str(current_datetime.year)
            current_index_date = current_datetime.weekday()
            if int(current_datetime_day) < 9: current_datetime_day = '0' + current_datetime_day
            if int(current_datetime_month) < 9: current_datetime_month = '0' + current_datetime_month 
            print(f"Today {current_datetime_day}.{current_datetime_month}.{current_datetime_year}")

            page.goto("https://e.mospolytech.ru/#/schedule/current", wait_until="networkidle")
            print(Style.RESET_ALL + 'processing')
            for _ in tqdm.tqdm(range(10)):
                sleep(0.35)

            html = page.content()
            soup = BeautifulSoup(html, "html.parser")
            array_links = []
            done_message = True

            day_divs = soup.find_all("div", class_="sc-1j9n86g-0 jxiZdc calendar-wrapper")
            if not day_divs or len(day_divs) < 6:
                print(Fore.RED + "Не удалось найти 6 div" + Style.RESET_ALL)
            
            current_day_div = day_divs[current_index_date]
            print(Fore.CYAN + f"Парсим расписание для дня с индексом {current_index_date}")

            for span in current_day_div.find_all("span", string=lambda s: s and "(Лекция)" in s):
                a_tag = span.find_previous("a", href=True)
                if a_tag:
                    if a_tag["href"] != "https://online.mospolytech.ru/":
                        array_links.append(a_tag["href"])
                else:
                    print(Fore.RED + "I don't see any link :(" + Style.RESET_ALL)
                    done_message = False

            if done_message:
                print(Fore.GREEN + 'ALL DONE!' + Style.RESET_ALL) 
                # print(f"array_links = {array_links}")

        except Exception as error:
            print(Fore.RED + f"Auth failed with error: {error}")

        browser.close()
        sleep(3)

        if len(array_links) != 0:
            try:
                webbrowser.open_new('https://google.com')
                sleep(3)
                for link in array_links:
                    webbrowser.open_new_tab(link)
                    sleep(5)

            except Exception as error:
                print(Fore.RED + f'Error! {error}')

            input(Style.RESET_ALL + "Press Enter to shutdown browser...")
            os.system("taskkill /im firefox.exe /f")
            os.system("taskkill /im chrome.exe /f")

        else:
            print(Fore.RED + "I don't see any link :(" + Style.RESET_ALL)
            sleep(2)
            print("Shutdown cmd proccess...")
            sleep(5)
            print("bye!")
            sleep(3)

def app():
    auth_and_parse()

app()