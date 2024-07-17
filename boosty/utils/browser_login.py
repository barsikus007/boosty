import json
from urllib.parse import unquote

from playwright._impl._api_structures import Cookie
from playwright.async_api import Request, async_playwright

from boosty.api.auth.resolvers.file import FileAuthDataResolver
from boosty.utils.consts import DEFAULT_USER_AGENT, LOGIN_URL
from boosty.utils.logging import logger
from boosty.utils.types import StrPath


async def log_handler(request: Request):  # TODO other types
    if not request.url.startswith("https://api.boosty.to/oauth/phone/token"):
        return

    logger.info(f"oauth/phone/token {request.post_data_json=}")
    resp = await request.response()
    if not resp:
        logger.error("Empty response")
        return
    logger.info(f"oauth/phone/token {await resp.json()=}")


async def retrieve_auth_cookies(*, user_agent: str) -> list[Cookie]:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(user_agent=user_agent)
        page = await context.new_page()
        page.on("request", log_handler)
        await page.goto(LOGIN_URL)

        button = page.locator('[data-test-id="COMMON_TOPMENU_TOPMENURIGHTUNAUTHORIZED\\:SIGN_IN"]')
        await button.click()
        await page.evaluate('alert("Auth and close window")')
        await page.pause()

        cookies = await context.cookies(LOGIN_URL)
        await browser.close()
        return cookies


async def interactive_login(
    *,
    force: bool = False,
    auth_file: StrPath = "auth.json",
    user_agent: str = DEFAULT_USER_AGENT,
) -> FileAuthDataResolver:
    auth_resolver = FileAuthDataResolver(auth_file=auth_file)
    if not force:
        auth_data = auth_resolver.load_auth_data()
        if not auth_data.anonymous:
            return auth_resolver

    cookies = await retrieve_auth_cookies(user_agent=user_agent)
    auth_cookies = {
        cookie.get("name"): unquote(cookie.get("value", ""))
        for cookie in cookies
        if cookie.get("name") in ["auth", "_clientId"]
    }

    auth_resolver.auth_data.from_cookies_data(json.loads(auth_cookies["auth"]))
    auth_resolver.auth_data.device_id = auth_cookies.get("_clientId")
    auth_resolver.auth_data.user_agent = user_agent
    logger.info(f"browser_login.{auth_resolver.auth_data=}")
    auth_resolver.save_auth_data()
    return auth_resolver
