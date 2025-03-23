from .transactions_page import TransactionsPage

from playwright.async_api import Page

class AccountPage:
    def __init__(self, page: Page):
        self.page = page

    async def get_welcome_text(self) -> str:
        return await self.page.inner_text(".fontBig")

    async def click_logout(self):
        await self.page.click("button[ng-click='byebye()']")

    async def get_balance(self) -> int:
        balance_text = await self.page.inner_text("div.center:has-text('Balance :')")
        balance = int(balance_text.split("Balance :")[1].split(",")[0].strip())
        return balance

    async def click_withdrawl(self):
        await self.page.click("button[ng-click='withdrawl()']")
        print("Clicked Withdrawl button")

    async def withdraw(self, amount: int):
        await self.page.fill("input[ng-model='amount']", str(amount))
        await self.page.click("button[type='submit'][value='']")
        print(f"Attempted to withdraw {amount}")

    async def click_deposit(self):
        await self.page.click("button[ng-click='deposit()']")
        print("Clicked Deposit button")

    async def deposit(self, amount: int):
        await self.page.fill("input[ng-model='amount']", str(amount))
        await self.page.click("button[type='submit'][value='']")
        print(f"Deposited {amount}")

    async def get_transaction_message(self) -> str:
        return await self.page.inner_text("span[ng-show='message']")
    
    async def click_transactions(self):
        await self.page.click("button[ng-click='transactions()']")
        # Wait for navigation to complete and transactions table to be visible
        await self.page.wait_for_selector("table.table-bordered", state="visible", timeout=10000)
        print("Clicked Transactions button")

    async def get_last_transactions(self, count: int = 2) -> list:
        # Wait for the table to be fully loaded
        await self.page.wait_for_selector("table.table-bordered", state="visible", timeout=10000)
        rows = await self.page.locator("table.table-bordered tbody tr").all()
        transactions = []
        
        # Check if there are any rows before trying to access them
        if not rows:
            print("No transactions found")
            return transactions
            
        # Only take the last 'count' rows, or all rows if there are fewer than 'count'
        recent_rows = rows[-min(count, len(rows)):]
        for row in recent_rows:
            date_time = await row.locator("td").nth(0).inner_text()
            amount = await row.locator("td").nth(1).inner_text()
            transaction_type = await row.locator("td").nth(2).inner_text()
            transactions.append({
                "date_time": date_time,
                "amount": amount,
                "transaction_type": transaction_type
            })
        return transactions