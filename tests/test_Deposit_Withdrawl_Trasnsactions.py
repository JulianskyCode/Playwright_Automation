import pytest
from playwright.async_api import async_playwright
from pages.login_page import LoginPage
from pages.account_page import AccountPage
from utils import utils

# Declare global variables for customer details
customer_name = None

async def select_random_customer(login_page):
    global customer_name
    customers = ["Hermoine Granger", "Harry Potter", "Ron Weasly", "Albus Dumbledore", "Neville Longbottom"]
    customer_name = utils.random_choice(customers)
    await login_page.select_customer(customer_name)
    print(f"Selected customer: {customer_name}")

@pytest.mark.asyncio
async def test_deposit_withdrawl_transactions():
    global customer_name

    async with async_playwright() as p:
        print("Launching browser...")
        browser = await p.chromium.launch(headless=True, slow_mo=100)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            # Navigate to login page and log in as customer
            login_page = LoginPage(page)
            await login_page.navigate()
            print("Navigated to login page")
            await login_page.click_customer_login()
            await select_random_customer(login_page)
            await login_page.click_login()
            print(f"Logged in as customer: {customer_name}")

            account_page = AccountPage(page)

            # Check balance
            balance = await account_page.get_balance()
            print(f"Current balance: {balance}")

            # Test withdrawl with amount higher than balance
            await account_page.click_withdrawl()
            await account_page.withdraw(balance + 100)
            message = await account_page.get_transaction_message()
            assert "Transaction Failed" in message, "Expected transaction failure message"
            print("Transaction failed as expected")

            # Test deposit
            await account_page.click_deposit()
            await account_page.deposit(100)
            message = await account_page.get_transaction_message()
            assert "Deposit Successful" in message, "Expected deposit success message"
            print("Deposit successful")

            # Test withdrawl with valid amount
            await account_page.click_withdrawl()
            await account_page.withdraw(50)
            message = await account_page.get_transaction_message()
            assert "Transaction successful" in message, "Expected transaction success message"
            print("Withdrawl successful")

            # Check last transactions
            await account_page.click_transactions()
            last_transactions = await account_page.get_last_transactions()
            for transaction in last_transactions:
                print(f"Transaction: Amount={transaction['amount']}, Type={transaction['transaction_type']}")
            assert last_transactions[-1]["amount"] == "50", "Expected last transaction amount to be 50"
            assert last_transactions[-1]["transaction_type"] == "Debit", "Expected last transaction type to be Debit"
            print("Last transaction validated successfully")

        finally:
            # Close the browser context
            await context.close()
            print("Closed browser context")