import asyncio
import logging

from boosty.api import API
from boosty.api.auth import Auth
from boosty.utils.browser_login import interactive_login

logger = logging.getLogger(__name__)


logging.basicConfig(level=logging.INFO)


async def main():
    # pip install boosty[browser]
    # playwright install chromium
    api = API(auth=Auth(await interactive_login()))
    response = await api.get_post("boosty", post_id="c9fb8a19-c45e-4602-9942-087c3af28c1b")
    logger.info(response.title)
    # 'Добро пожаловать на борт!'


if __name__ == "__main__":
    asyncio.run(main())
