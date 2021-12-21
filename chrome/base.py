# coding=utf-8

import os
import time
import traceback
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebElement, WebDriver
from selenium.webdriver.support import expected_conditions as EC

with open(os.path.join(os.getcwd(), "chrome", "stealth.min.js"), encoding="UTF-8") as f:
    js = f.read()


class ElementConfig:

    def __init__(self, xpath, is_frame=False, retry=3, retry_seconds=1, finish_seconds=1):
        self.xpath = xpath
        self.is_frame = is_frame
        self.retry = retry
        self.retry_seconds = retry_seconds
        self.finish_seconds = finish_seconds


class Chrome:
    __wait = 5

    def __init__(self, server=False, is_headless=1, crx=None):

        options = webdriver.ChromeOptions()
        if server:
            options.debugger_address = server
        else:
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument('--log-level=2')
            options.add_argument("--disable-logging")
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-popup-blocking')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox ')
            if not is_headless:
                options.add_argument('--headless')

            for x in crx or []: options.add_extension(x)

        self._driver = webdriver.Chrome(executable_path=os.path.join(os.getcwd(), "chrome", "chromedriver.exe"), options=options)
        self._driver.implicitly_wait(self.__wait)
        self._driver_wait = WebDriverWait(self._driver, self.__wait)
        self._driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})
        self.frame_layers = 0

    def close(self):
        try:
            self.driver.quit()
        except:
            traceback.print_exc()

    @property
    def driver(self) -> WebDriver:
        return self._driver

    def execute_script(self, script, cla=None, finish_seconds=0):
        self.driver.execute_script(script, cla) if cla else self.driver.execute_script(script)
        time.sleep(finish_seconds)
        return True

    def _get_element_of_frame(self, ele: ElementConfig):

        self._driver.implicitly_wait(0)

        def _get_element(self, xpath):

            def _switch_to_frame(self, xpath):
                frame_ls = self._driver.find_elements_by_tag_name('iframe') or self._driver.find_elements_by_tag_name('frame')
                for frame in frame_ls:
                    self._driver.switch_to.frame(frame)
                    self.frame_layers += 1
                    elements = _get_element(self, xpath)
                    if elements:
                        return elements
                    else:
                        self._driver.switch_to.parent_frame()
                        self.frame_layers -= 1

            elements = self._driver.find_elements_by_xpath(xpath)
            if not elements:
                elements = _switch_to_frame(self, xpath)
            return elements

        elements = None
        while ele.retry:
            elements = _get_element(self, ele.xpath)
            if elements:
                break
            ele.retry -= 1
            time.sleep(ele.retry_seconds)

        self._driver.implicitly_wait(self.__wait)

        return elements

    def _wait_element(self, ele: ElementConfig):
        try:
            element = self._driver_wait.until(EC.presence_of_all_elements_located((By.XPATH, ele.xpath)))
        except:
            element = None
            traceback.print_exc()
        return element

    def get_element(self, ele: ElementConfig) -> [WebElement]:
        if ele.is_frame:
            element = self._get_element_of_frame(ele)
        else:
            element = self._wait_element(ele)
        return element

    def my_func(self, func):
        return func(self)

    def set_cookies(self, url, cookies):
        domain = urlparse(url).netloc.replace("www.", "")
        if isinstance(cookies, str):
            cookies = {c.split("=", 1)[0]: c.split("=", 1)[1] for c in cookies.strip().split("; ")}
        cookies = [
            {"name": key, "value": value.strip(), "path": "/", "domain": ".{}".format(domain)}
            for key, value in cookies.items()
        ]
        # self.driver.delete_all_cookies()
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        return True

    def get_cookies(self):
        return self._driver.get_cookies()

    def get(self, url):
        self.driver.get(url)
        return True

    def input(self, ele: ElementConfig, text):
        element = self.get_element(ele)
        if element:
            element[0].send_keys(Keys.CONTROL, 'a')
            element[0].send_keys(text)
            time.sleep(ele.finish_seconds)
            return True

    def select(self, ele: ElementConfig, text):
        element = self.get_element(ele)
        if element:
            Select(element[0]).select_by_visible_text(text)
            return True

    def click(self, ele: ElementConfig):
        element = self.get_element(ele)
        if element:
            self.execute_script("arguments[0].click();", element[0], ele.finish_seconds)
            return True

    def node_html(self, ele: ElementConfig):
        element = self.get_element(ele)
        if element:
            return element[0].get_attribute("outerHTML")

    def switch_window(self, close=False):
        if close:
            self._driver.close()
        self._driver.switch_to.window(self._driver.window_handles[-1])
        return True
