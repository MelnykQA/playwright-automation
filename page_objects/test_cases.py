from playwright.sync_api import Page

class TestCases:
    def __init__(self, page: Page):
        self.page = page

    def check_test_exists(self, test_name: str):
        return self.page.query_selector(f'css=tr >> text=\"{test_name}\"') is not None

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


    def check_columns_hidden(self):
        description = self.page.is_hidden('.thDes')
        author = self.page.is_hidden('.thAuthor')
        executor = self.page.is_hidden('.thLast')
        return description and author and executor