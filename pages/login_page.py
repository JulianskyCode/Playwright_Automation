from playwright.async_api import Page
from .manager_page import ManagerPage
from .customers_page import CustomersPage

class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    async def navigate(self):
        await self.page.goto("https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login")
        print("I ran navigate functions")

    async def click_customer_login(self):
        await self.page.click("text=Customer Login")

    async def select_customer(self, name: str):
        await self.page.select_option("select[name='userSelect']", label=name)

    async def click_login(self):
        await self.page.click("button[type='submit']")

    async def login_as_customer(self, customer_name: str) -> CustomersPage:
        await self.click_customer_login()
        await self.select_customer(customer_name)
        await self.click_login()
        return CustomersPage(self.page)
    
    async def login_as_manager(self):
        print("Attempting to wait for manager login button")
        await self.page.wait_for_selector("text=Bank Manager Login", timeout=10000)
        print("Manager login button is visible")
        await self.page.click("text=Bank Manager Login")
        print("Manager login button clicked")

    async def is_login_page_displayed(self) -> bool:
        customer_button = await self.page.query_selector("text=Customer Login")
        manager_button = await self.page.query_selector("text=Bank Manager Login")
        return customer_button is not None and manager_button is not None