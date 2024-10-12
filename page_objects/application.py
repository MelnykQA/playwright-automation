import logging
from playwright.sync_api import Browser
from playwright.sync_api import Request, Route, ConsoleMessage, Dialog
from .test_cases import TestCases
from .demo_pages import DemoPages

class App:
    def __init__(self, browser: Browser, base_url: str, **kwargs):
        self.browser = browser
        self.context = self.browser.new_context(**kwargs)
        self.page = self.context.new_page()
        self.base_url = base_url
        self.test_cases = TestCases(self.page)
        self.demo_pages = DemoPages(self.page)

        def console_handler(message: ConsoleMessage):
            if message.type == 'error':
                logging.error(f'page: {self.page.url}, console error: {message.text}')
        def dialog_handler(dialog: Dialog):
            logging.warning(f'page: {self.page.url}, dialog text: {dialog.message}')
            dialog.accept()

        self.page.on('console', console_handler)
        self.page.on('dialog', dialog_handler)

    def goto(self, endpoint: str, use_base_url=True):
        if use_base_url:
            self.page.goto(self.base_url + endpoint)
        else:
            self.page.goto(endpoint)

    def navigate_to(self, menu: str):
        self.page.click(f"css=header >> text=\"{menu}\"")
        self.page.wait_for_load_state()

    def login(self, login: str, password: str):
        self.page.fill("input[name=\"username\"]", login)
        self.page.fill("input[name=\"password\"]", password)
        self.page.press("input[name=\"password\"]", "Enter")

    def create_test(self, test_name: str, test_description: str):
        self.page.fill("input[name=\"name\"]", test_name)
        self.page.get_by_label("Test description").click()
        self.page.get_by_label("Test description").fill(test_description)
        # self.page.fill("input[name=\"description\"]", test_description)
        self.page.click("input[type=\"submit\"]")


    def check_test_exists(self, test_name: str):
        return self.page.query_selector(f'css=tr >> text=\"{test_name}\"') is not None

    #def delete_test_by_name(self, test_name: str):
        #row = self.page.query_selector(f'*css=tr >> text=\"{test_name}\"')
        #row.query_selector('button = \"{Delete}\"').click()
        #self.page.get_by_role("row", name="{test_name}").get_by_role("button").nth(3).click()
        #self.page.get_by_role("row", name=test_name).get_by_role("button").nth(3).click()

    def delete_test_by_name(self, test_name: str):
        # Знаходимо рядок, що містить назву тесту
        row = self.page.get_by_role("row", name=test_name)

        # Перевіряємо, чи знайдено рядок
        if row:
            # Знаходимо кнопку видалення всередині рядка і натискаємо її
            delete_button = row.get_by_role("button").nth(3)
            if delete_button:
                delete_button.click()
            else:
                print("Кнопка видалення не знайдена.")
        else:
            print("Рядок з назвою тесту не знайдено.")


    def click_menu_button(self):
        self.page.wait_for_selector('.menuBtn')
        self.page.click('.menuBtn')

    def is_menu_button_visible(self):
        return self.page.is_visible('.menuBtn')

    def get_location(self):
        return self.page.text_content('.position')

    def intercept_requests(self, url: str, payload: str):
        def handler(route: Route, request: Request):
            route.fulfill(status=200, body=payload)

        self.page.route(url, handler)

    def stop_intercept(self, url: str):
        self.page.unroute(url)

    def refresh_dashboard(self):
        self.page.click('input')

    def get_total_tests_stats(self):
        return self.page.text_content('.total >> span')

    def close(self):
        self.page.close()
        self.context.close()

