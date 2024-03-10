import json

import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import undetected_chromedriver as uс
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from urllib.parse import unquote
import random

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 "
                  "Safari/537.36"
}


def get_source_html(url):
    driver = None
    try:
        driver = uс.Chrome()
        driver.maximize_window()
        driver.get(url)
        time.sleep(3)
        flag_end = 0
        while True:
            find_more_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "list-rating-info"))
            )
            action = ActionChains(driver)
            action.move_to_element(find_more_element).perform()
            time.sleep(2)
            print("1")
            if flag_end or driver.find_elements(By.CLASS_NAME, "hasmore-text"):
                print("4")
                with open("C:\\Users\\qwer7\\PycharmProjects\\parserZoon\\source-page2.html", "w",
                          encoding="utf-8") as file:
                    file.write(driver.page_source)
                    break
            else:
                print("2")
                try:
                    button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "button-show-more"))
                    )
                    if button:
                        print("3")
                        action.click(button).perform()
                except:
                    flag_end = 1
                finally:
                    time.sleep(1)



    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def get_items_urls(file_path):
    with open(file_path, encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    items_divs = soup.find_all("div", {"class": "minicard-item__info"})

    urls = []
    for item in items_divs:
        item_url = item.find("h2", {"class": "minicard-item__title"}).find("a").get("href")
        urls.append(item_url)

    with open("C:\\Users\\qwer7\\PycharmProjects\\parserZoon\\items_urls2.txt", "w", encoding="utf-8") as file:
        for url in urls:
            file.write(f"{url}\n")

    return "[INFO] Urls collected successfully!"


def get_data(file_path):
    with open(file_path, encoding="utf-8") as file:


        urls_list = [url.strip() for url in file.readlines()]

    result_list = []
    urls_count = len(urls_list)
    count = 1
    for url in urls_list:
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")

        try:
            item_name = soup.find("span", {"itemprop": "name"}).text.strip()
        except Exception as _ex:
            item_name = None

        item_phone_list = []
        try:
            item_phones = soup.find("div", {"class": "service-phones-list"}).find_all("a", {"class": "js-phone-number"})

            for phone in item_phones:
                item_phone = phone.get("href").split(":")[-1].strip()
                item_phone_list.append(item_phone)
        except Exception as _ex:
            item_phone_list = None

        try:
            item_address = soup.find("address", {"class": "iblock"}).text.strip()
        except Exception as _ex:
            item_address = None

        try:
            item_site = soup.find("div", {"class": "service-website-value"}).text.strip()
        except Exception as _ex:
            item_site = None

        social_networks_list = []
        try:
            item_social_networks = soup.find("div", {"class": "service-description-social-list"}).find_all("a", {
                "class": "service-description-social-btn"})
            for sn in item_social_networks:
                sn_url = sn.get("href")
                sn_url = unquote(sn_url.split("?to=")[1].split("&")[0])
                social_networks_list.append(sn_url)
        except Exception as _ex:
            social_networks_list = None

        result_list.append(
            {
                "item_name": item_name,
                "item_url": url,
                "item_phone_list": item_phone_list,
                "item_address": item_address,
                "item_site": item_site,
                "social_networks_list": social_networks_list
            }
        )
        time.sleep(random.randrange(1, 2))

        if count % 10 == 0:
            time.sleep(random.randrange(1, 2))

        print(f"[+] Processed: {count}/{urls_count}")

        count += 1

    with open("C:\\Users\\qwer7\\PycharmProjects\\parserZoon\\result2.json", "w", encoding="utf-8") as file:
        json.dump(result_list, file, indent=4, ensure_ascii=False)

    return "[INFO] Data collected successfully!"


def main():
    get_source_html("https://zoon.ru/spb/kindergarten/?search_query_form=1&m%5B5228936340c088ae2a8b457a%5D=1&center"
                    "%5B%5D=60.0360140861141&center%5B%5D=30.538349471523613&zoom=13")
    print(get_items_urls(file_path="C:\\Users\\qwer7\\PycharmProjects\\parserZoon\\source-page2.html"))
    print(get_data(file_path="C:\\Users\\qwer7\\PycharmProjects\\parserZoon\\items_urls2.txt"))


if __name__ == "__main__":
    main()
