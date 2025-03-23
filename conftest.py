# import pytest
# from playwright.async_api import async_playwright

# @pytest.fixture(scope="session")
# async def browser():
#     async with async_playwright() as p:
#         # Launch browser (non-headless for debugging; adjust slow_mo if needed)
#         browser = await p.chromium.launch(headless=False, slow_mo=1000)
#         yield browser
#         await browser.close()

# @pytest.fixture(scope="session")
# async def browser_context(browser):
#     context = await browser.new_context()
#     yield context
#     await context.close()

# @pytest.fixture(scope="session")
# async def page(browser_context):
#     page = await browser_context.new_page()
#     yield page
#     await page.close()


# import pytest
# from playwright.async_api import async_playwright

# @pytest.fixture(scope="function")
# async def temporary_page():
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=False, slow_mo=1000)
#         context = await browser.new_context()
#         page = await context.new_page()
#         yield page
#         await page.close()
#         await context.close()
#         await browser.close()

# @pytest.fixture(scope="session")
# async def browser_context(browser):
#     # Keep context open during session
#     context = await browser.new_context()
#     yield context
#     # Do NOT close context here

# @pytest.fixture(scope="session")
# async def page(browser_context):
#     # Create and keep a single page open for the whole session
#     page = await browser_context.new_page()
#     yield page
#     # Do NOT close page here