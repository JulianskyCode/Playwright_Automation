import pytest
from playwright.async_api import async_playwright
from pages.login_page import LoginPage
from pages.manager_page import ManagerPage
from pages.customers_page import CustomersPage  # Assuming you have a CustomerPage class for customer login
from utils import utils

# Declare global variables for customer details
first_name = None
last_name = None
post_code = None

# Declare URL variables
manager_list_url = "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/manager/list"

async def generate_customer_details():
    global first_name, last_name, post_code
    first_name = utils.generate_first_name()
    last_name = utils.generate_last_name()
    post_code = utils.generate_postcode()
    print(f"Generated customer details: First Name: {first_name}, Last Name: {last_name}, Post Code: {post_code}")

async def add_customer(manager_page):
    await manager_page.click_add_customer()
    print("Clicked Add Customer button")

    # Fill in and submit the customer details
    await manager_page.fill_customer_details(first_name, last_name, post_code)
    print("Filled customer details")
    await manager_page.submit_add_customer()
    print("Submitted customer details")

    # Verify that the input fields are empty
    fields_empty = await manager_page.are_fields_empty()
    print(f"Fields empty: {fields_empty}")
    assert fields_empty, "Input fields are not empty after submitting the form"

async def search_customer(page):
    # Navigate to the customer list page
    await page.goto(manager_list_url)
    print("Navigated to customer list page")
    
    # Search using the postcode
    await page.fill('input[ng-model="searchCustomer"]', post_code)
    print(f"Searched for customer with Post Code: {post_code}")
    # Wait briefly for the table to filter (adjust timeout as needed)
    await page.wait_for_timeout(500)
    
    # Get all visible table rows
    rows = await page.locator('tbody tr').all()
    print(f"Found {len(rows)} rows in the table")
    found = False
    for row in rows:
        cells = await row.locator('td').all()
        cell_texts = [await cell.inner_text() for cell in cells]
        print(f"Row cells: {cell_texts}")
        if len(cells) >= 3:  # Ensure row has at least First Name, Last Name, Post Code
            fn = await cells[0].inner_text()
            ln = await cells[1].inner_text()
            pc = await cells[2].inner_text()
            if (fn == first_name and 
                ln == last_name and 
                pc == post_code):
                found = True
                break
    
    # Assert that the customer was found
    assert found, f"Customer with First Name: {first_name}, Last Name: {last_name}, Postcode: {post_code} not found in the list"
    print(f"Customer '{first_name} {last_name}' found in the list")

async def login_as_customer(login_page, customer_page):
    # Navigate to login page and log in as customer
    await login_page.navigate()
    print("Navigated to login page")
    await login_page.click_customer_login()
    print("Clicked Customer Login button")

    await customer_page.login(f"{first_name} {last_name}")
    print(f"Logged in as customer: {first_name} {last_name}")

    # Verify successful login (you may need to adjust this based on your application's behavior)
    is_logged_in = await customer_page.is_logged_in()
    print(f"Customer login successful: {is_logged_in}")
    assert is_logged_in, "Customer login failed"

@pytest.mark.asyncio
async def test_add_search_and_login_customer():
    global first_name, last_name, post_code

    """
    Test to add a new customer, search for the customer in the list, and log in as the customer.
    Uses randomly generated customer details from utils.py.
    Verifies that the form fields are cleared after submission,
    the customer appears in the list, and the customer can log in successfully.
    """
    await generate_customer_details()

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

            # Verify the Add Customer button is present
            manager_page = ManagerPage(page)
            is_button_present = await manager_page.is_add_customer_button_present()
            print(f"Add Customer button present: {is_button_present}")
            assert is_button_present, "Add Customer button not found"

            # Add customer
            await add_customer(manager_page)

            # Search for customer
            await search_customer(page)

            # Log in as customer
            customer_page = CustomersPage(page)
            await login_as_customer(login_page, customer_page)

        finally:
            # Close the browser context
            await context.close()
            print("Closed browser context")