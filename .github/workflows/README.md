# GitHub Actions Daily Test Setup

## Setup Details

1. Created a `.github/workflows/daily-tests.yml` file with the following configuration:
   - Schedule: Daily at midnight UTC
   - Manual trigger option via `workflow_dispatch`
   - Runs on Ubuntu latest
   - Uses Python 3.10
   - Installs required dependencies and Playwright browsers
   - Runs the tests with pytest

2. Created a `requirements.txt` file with the necessary dependencies:
   - pytest
   - pytest-asyncio
   - playwright
   - python-dotenv

## How this works

- The workflow will automatically run every day at midnight UTC
- You can also trigger the workflow manually from the GitHub Actions tab
- It will install the required dependencies, including the Playwright browsers
- Then it will run all the tests in your `tests/` directory
