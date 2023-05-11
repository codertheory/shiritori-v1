import pytest

from .locators import HomePageLocators


@pytest.mark.asyncio
@pytest.mark.e2e
async def test_live_server(puppeteer_browser):
    browser, page = puppeteer_browser
    assert puppeteer_browser is not None
    # Enter username
    await page.waitFor(2000)  # Wait for page to load
    await page.waitForSelector(HomePageLocators.USER_NAME_INPUT)
    await page.type(HomePageLocators.USER_NAME_INPUT, "Jane")

    # Assert that username is entered
    username = await page.evaluate("document.querySelector('input[name=username]').value")
    assert username == "Jane"

    # TODO: Finish this test
    # # Submit Form
    # await asyncio.gather(
    #     page.waitForNavigation(),
    #     page.click("button[type=submit]")
    # )
    #
    # # # Create game
    # # await page.waitForSelector(HomePageLocators.CREATE_GAME_BUTTON)
    # # await asyncio.gather(
    # #     page.waitForNavigation(),
    # #     page.click(HomePageLocators.CREATE_GAME_BUTTON)
    # # )
    # # Wait for game page to load
    # # Check that game page is loaded
    # assert "game" in page.url
