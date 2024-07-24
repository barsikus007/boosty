import asyncio

from boosty.api import API


async def main():
    api = API()
    response = await api.get_post("boosty", post_id="c9fb8a19-c45e-4602-9942-087c3af28c1b")
    print(response.title)
    # 'Добро пожаловать на борт!'
    print(response.url)
    # 'https://boosty.to/boosty/posts/c9fb8a19-c45e-4602-9942-087c3af28c1b'


if __name__ == "__main__":
    asyncio.run(main())
