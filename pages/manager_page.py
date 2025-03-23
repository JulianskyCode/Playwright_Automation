from playwright.async_api import Page
from utils import test_data

class ManagerPage:
    def __init__(self, page: Page):
        self.page = page

    async def is_add_customer_button_present(self):
        is_visible = await self.page.is_visible('button[ng-click="addCust()"]')
        print(f"Add Customer button visible: {is_visible}")
        return is_visible

    async def click_add_customer(self):
        print("Waiting for Add Customer button to be visible")
        await self.page.wait_for_selector('button[ng-click="addCust()"]', state='visible')
        print("Clicking Add Customer button")
        await self.page.click('button[ng-click="addCust()"]')
        await self.page.wait_for_selector('form[name="myForm"]', state='visible')  # Wait for the form to be visible

    async def fill_customer_details(self, first_name, last_name, post_code):
        print("Waiting for first name input field")
        await self.page.wait_for_selector('input[ng-model="fName"]')  # Update the selector as needed
        print("Filling first name")
        await self.page.fill('input[ng-model="fName"]', first_name)
        print("Filling last name")
        await self.page.fill('input[ng-model="lName"]', last_name)
        print("Filling post code")
        await self.page.fill('input[ng-model="postCd"]', post_code)

    async def submit_add_customer(self):
        print("Submitting customer details")
        await self.page.click('button[type="submit"]')
        print(f"Customer details submitted '{test_data.first_name} {test_data.last_name}'")

    async def are_fields_empty(self):
        first_name_value = await self.page.input_value('input[ng-model="fName"]')
        last_name_value = await self.page.input_value('input[ng-model="lName"]')
        post_code_value = await self.page.input_value('input[ng-model="postCd"]')
        return first_name_value == "" and last_name_value == "" and post_code_value == ""

    async def click_open_account(self):
        await self.page.click("button[ng-click='openAccount()']")
        print("Clicked Open Account button")

    async def select_customer(self, customer_name: str):
        await self.page.select_option("select[name='userSelect']", label=customer_name)
        print(f"Selected customer: {customer_name}")

    async def select_currency(self, currency: str):
        await self.page.select_option("select[name='currency']", label=currency)
        print(f"Selected currency: {currency}")

    async def click_process(self):
        await self.page.click("button[type='submit'][value='']")
        print("Clicked Process button")

    async def get_account_number_from_alert(self) -> str:
        dialog = await self.page.wait_for_event("dialog")
        message = dialog.message
        await dialog.accept()
        account_number = message.split("Account created successfully with account Number ")[1].strip()
        return account_number

    async def click_customers_tab(self):
        await self.page.click("button[ng-click='showCust()']")
        print("Clicked Customers tab")

    async def search_customer(self, search_term: str):
        await self.page.fill("input[ng-model='searchCustomer']", search_term)
        print(f"Searched for customer: {search_term}")

    async def get_account_numbers(self, search_term: str) -> list:
        rows = await self.page.locator(f"tr:has-text('{search_term}')").all()
        account_numbers = []
        for row in rows:
            account_number = await row.locator("td").nth(3).inner_text()  # Assuming the account number is in the 4th column
            account_numbers.append(account_number)
        return account_numbers
    
    async def select_customer_by_first_name(self, first_name: str):
        options = await self.page.locator("select[name='userSelect'] option").all_text_contents()
        for option in options:
            if first_name in option:
                await self.page.select_option("select[name='userSelect']", label=option)
                print(f"Selected customer: {option}")
                break