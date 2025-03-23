import pytest
from playwright.async_api import async_playwright
from pages.login_page import LoginPage
from pages.manager_page import ManagerPage
from utils import utils

# Declare global variables for customer details
customer_name = None
currency = None

async def select_random_customer(manager_page):
    global customer_name
    customers = ["Hermoine Granger", "Harry Potter", "Ron Weasly", "Albus Dumbledore", "Neville Longbottom"]
    customer_name = utils.random_choice(customers)
    await manager_page.select_customer_by_first_name(customer_name.split()[0])
    print(f"Selected customer: {customer_name}")

async def select_random_currency(manager_page):
    global currency
    currencies = ["Dollar", "Pound", "Rupee"]
    currency = utils.random_choice(currencies)
    await manager_page.select_currency(currency)
    print(f"Selected currency: {currency}")

@pytest.mark.asyncio
async def test_create_account():
    global customer_name, currency

    async with async_playwright() as p:
        print("Launching browser...")
        browser = await p.chromium.launch(headless=True, slow_mo=100)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            # Navigate to login page and log in as manager
            login_page = LoginPage(page)
            await login_page.navigate()
            print("Navigated to login page")
            await login_page.login_as_manager()
            print("Logged in as manager")

            manager_page = ManagerPage(page)

            # Navigate to Customers tab
            await manager_page.click_customers_tab()

            # Pick a random customer by first name from the customers list
            customers = ["Hermoine", "Harry", "Ron", "Albus", "Neville"]
            first_name = utils.random_choice(customers)
            print(f"Selected customer first name: {first_name}")

            # Search for the customer by first name
            await manager_page.search_customer(first_name)
            account_numbers_before = await manager_page.get_account_numbers(first_name)
            print(f"Account numbers for {first_name} before opening account: {account_numbers_before}")

            # Open account
            await manager_page.click_open_account()

            # Select the same customer and a random currency
            await manager_page.select_customer_by_first_name(first_name)
            await select_random_currency(manager_page)

            # Process account creation
            await manager_page.click_process()

            # Navigate to Customers tab again
            await manager_page.click_customers_tab()

            # Search for the customer again by first name
            await manager_page.search_customer(first_name)
            account_numbers_after = await manager_page.get_account_numbers(first_name)

            # Validate that new account numbers are present
            new_account_numbers = set(account_numbers_after) - set(account_numbers_before)
            assert len(new_account_numbers) == 1, f"Expected one new account number, but found {len(new_account_numbers)}"
            new_account_number = new_account_numbers.pop()
            print(f"Last one is the newly created account number for {first_name}: {new_account_number}")

        finally:
            # Close the browser context
            await context.close()
            print("Closed browser context")