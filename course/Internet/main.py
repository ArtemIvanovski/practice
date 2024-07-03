from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time


class WebDriverManager:
    def __init__(self, driver_path, headless=True):
        self.driver_path = driver_path
        self.headless = headless
        self.driver = self._initialize_driver()

    def _initialize_driver(self):
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")

        service = Service(self.driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def open_url(self, url):
        self.driver.get(url)
        time.sleep(1)

    def set_local_storage(self, key, value):
        set_script = f"window.localStorage.setItem('{key}', '{value}');"
        self.driver.execute_script(set_script)

    def get_local_storage(self, key):
        get_script = f"return window.localStorage.getItem('{key}');"
        return self.driver.execute_script(get_script)

    def remove_local_storage(self, key):
        remove_script = f"window.localStorage.removeItem('{key}');"
        self.driver.execute_script(remove_script)

    def set_cookie(self, name, value):
        self.driver.add_cookie({"name": name, "value": value})

    def get_cookie(self, name):
        cookie = self.driver.get_cookie(name)
        return cookie['value'] if cookie else None

    def delete_cookie(self, name):
        self.driver.delete_cookie(name)

    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    chrome_driver_path = 'C://Users/Pasha/Desktop/chromedriver.exe'
    url = 'https://example.com'
    local_storage_key = 'myKey'
    local_storage_value = 'myValue'
    cookie_name = 'myCookie'
    cookie_value = 'cookieValue'

    web_driver_manager = WebDriverManager(chrome_driver_path, headless=False)

    try:
        web_driver_manager.open_url(url)

        web_driver_manager.set_local_storage(local_storage_key, local_storage_value)
        print(f"Set LocalStorage: {local_storage_key} = {local_storage_value}")

        stored_value = web_driver_manager.get_local_storage(local_storage_key)
        print(f"Stored value in LocalStorage: {stored_value}")

        web_driver_manager.remove_local_storage(local_storage_key)
        stored_value = web_driver_manager.get_local_storage(local_storage_key)
        print(f"Stored value in LocalStorage after removal: {stored_value}")

        web_driver_manager.set_cookie(cookie_name, cookie_value)
        print(f"Set Cookie: {cookie_name} = {cookie_value}")

        stored_cookie = web_driver_manager.get_cookie(cookie_name)
        print(f"Stored value in Cookie: {stored_cookie}")

        web_driver_manager.delete_cookie(cookie_name)
        stored_cookie = web_driver_manager.get_cookie(cookie_name)
        print(f"Stored value in Cookie after removal: {stored_cookie}")

    finally:
        web_driver_manager.close()
