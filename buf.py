import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time


def get_source_html(url):
    driver = webdriver.Firefox()
    driver.maximize_window()

    try:
        driver.get(url)
        time.sleep(3)

        while True:
            find_more_element = driver.find_element(By.CLASS_NAME, "catalog-button-showMore")
            if driver.find_elements(By.CLASS_NAME, "hasmore-text"):
                with open("parcerZoon/source-page.html", "w") as file:
                    file.write(driver.page_source)
                    break
            else:
                action = ActionChains(driver)
                action.move_to_element(find_more_element).perform()
                time.sleep(3)
    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()


def main():
    get_source_html(
        url="https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html")


if __name__ == "__main__":
    main()
