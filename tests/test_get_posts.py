import pytest

from boosty.api import API


pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio(scope="module")
async def test_get_specific_post():
    api = API()
    response = await api.get_post("boosty", post_id="c9fb8a19-c45e-4602-9942-087c3af28c1b")
    assert response.title == "Добро пожаловать на борт!"


@pytest.mark.asyncio(scope="module")
async def test_get_all_posts():
    api = API()
    response = await api.get_posts("boosty")
    assert len(response.data) == 100
