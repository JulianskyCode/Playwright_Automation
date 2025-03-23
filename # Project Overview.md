# Project Overview

This project automates various functionalities of the angularJs-protractor application (https://www.globalsqa.com/angularJs-protractor/BankingProject) using Playwright. The project is structured into different modules for pages, tests, and utilities.

## Project Structure

### Pages
- **login_page.py**: Contains methods for navigating to the login page and logging in as a customer or manager.
- **manager_page.py**: Contains methods for interacting with the manager functionalities, such as adding customers, opening accounts, selecting customers, and navigating to the Customers tab.
- **customers_page.py**: Contains methods for interacting with customer functionalities, such as checking if a customer is present, deleting a customer, logging in as a customer, and verifying successful login.
- **account_page.py**: Contains methods for interacting with account functionalities, such as checking balance, performing deposits and withdrawals, and viewing transactions.

### Tests
- **test_Create_Account.py**: This test script validates the process of creating a new account for a randomly selected customer. It includes steps to:
  - **Login as Manager**: Navigates to the login page and logs in as a manager.
  - **Retrieve Existing Account Numbers**: Navigates to the Customers tab and retrieves the existing account numbers for a randomly selected customer by first name.
  - **Open New Account**: Opens the account creation form, selects the same customer, and a random currency, then processes the account creation.
  - **Verify New Account**: Navigates back to the Customers tab, retrieves the updated list of account numbers for the customer, and verifies that a new account number has been created.

- **test_Create_Search_Login.py**: This test script validates the process of adding a new customer, searching for the customer in the list, and logging in as the customer. It includes steps to:
  - **Generate Customer Details**: Generates random customer details (first name, last name, and post code) using utility functions.
  - **Login as Manager**: Navigates to the login page and logs in as a manager.
  - **Add Customer**: Verifies the presence of the Add Customer button, fills in the customer details, submits the form, and verifies that the input fields are cleared.
  - **Search for Customer**: Navigates to the customer list page, searches for the customer using the post code, and verifies that the customer appears in the list.
  - **Login as Customer**: Logs in as the newly added customer and verifies successful login.

- **test_Deposit_Withdrawl_Transactions.py**: This test script validates the process of performing deposit and withdrawal transactions for a randomly selected customer. It includes steps to:
  - **Login as Customer**: Navigates to the login page, logs in as a customer, and selects a random customer from a predefined list.
  - **Check Balance**: Retrieves and prints the current balance of the customer.
  - **Test Withdrawal with Amount Higher than Balance**: Attempts to withdraw an amount higher than the current balance and verifies that the transaction fails.
  - **Test Deposit**: Deposits a specified amount into the customer's account and verifies that the deposit is successful.
  - **Test Withdrawal with Valid Amount**: Withdraws a valid amount from the customer's account and verifies that the transaction is successful.
  - **Check Last Transactions**: Retrieves and prints the last transactions, and verifies that the last transaction matches the expected amount and type.

### Utilities
- **utils.py**: Contains utility functions that assist with random selections and other helper methods used across the tests. Examples include:
  - **generate_first_name()**: Generates a random first name.
  - **generate_last_name()**: Generates a random last name.
  - **generate_postcode()**: Generates a random post code.
  - **random_choice(list)**: Selects a random item from a given list.

## Running the Tests
Use `pytest` to run the tests in the `tests` folder:
```sh
pytest -s tests/