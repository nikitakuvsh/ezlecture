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
            if current_datetime.month < 10: print(f"Today {current_datetime.day}.0{current_datetime.month}.{current_datetime.year}")
            else: print(f"Today {current_datetime.day}.{current_datetime.month}.{current_datetime.year}")

            page.goto("https://e.mospolytech.ru/#/schedule/current", wait_until="networkidle")
            print(Style.RESET_ALL + 'processing')
            for _ in tqdm.tqdm(range(10)):
                sleep(0.35)

            html = page.content()
            soup = BeautifulSoup(html, "html.parser")
            array_links = []
            done_message = True

            for span in soup.find_all("span", string=lambda s: s and "(Лекция)" in s):
                a_tag = span.find_previous("a", href=True)
                if a_tag:
                    if a_tag["href"] != "https://online.mospolytech.ru/":
                        array_links.append(a_tag["href"])
                else:
                    print(Fore.RED + "I don't see anyone link :(")
                    done_message = False

            if done_message:
                print(Fore.GREEN + 'ALL DONE!') 
                # print(f"array_links = {array_links}")

        except Exception as error:
            print(Fore.RED + f"Auth failed with error: {error}")

        browser.close()
        sleep(50)
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

def app():
    auth_and_parse()

app()