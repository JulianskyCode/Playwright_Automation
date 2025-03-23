from playwright.async_api import Page

class CustomersPage:
    def __init__(self, page: Page):
        self.page = page

    async def is_customer_present(self, name: str) -> bool:
        count = await self.page.locator(f"td:has-text('{name}')").count()
        return count > 0

    async def delete_customer(self, name: str):
        await self.page.locator(f"tr:has-text('{name}') button[ng-click='deleteCust(cust)']").click()

    async def login(self, customer_name: str):
        # Log the available options in the dropdown
        options = await self.page.locator("select[name='userSelect'] option").all_text_contents()
        print(f"Available options: {options}")

        # Attempt to select the customer name
        await self.page.select_option("select[name='userSelect']", label=customer_name)
        await self.page.click("button[type='submit']")

    async def is_logged_in(self):
        # Verify successful login by checking for a specific element that appears after login
        return await self.page.is_visible('button[ng-click="byebye()"]')
    
    async def get_welcome_text(self) -> str:
        return await self.page.inner_text("selector-for-welcome-text")

    async def click_logout(self):
        await self.page.click("button[ng-click='byebye()']")