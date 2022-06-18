import asyncio

import requests

from backend.core.database import async_session
from backend.mem.repository import MemRepository
from backend.mem.schemas import MemInCreatePydantic


def get_links(owner_id, album_id):
    response = requests.get(
        'https://api.vk.com/method/photos.get',
        params={
            'access_token': '463f8122463f8122463f81229d464293c64463f463f81222492cbe1cde3e891a675a67a',
            'v': '5.131',
            'owner_id': owner_id,
            'album_id': album_id,
            'count': 100
        }
    )
    items = response.json()['response']['items']
    links_selected = []
    for item in items:
        url = list(filter(lambda x: x['width'] >= 300, item['sizes']))[0]['url']
        links_selected.append(url)
    return links_selected


links = get_links('-197700721', '281940823') + \
        get_links('-71711391', '276277792')

# https://vk.com/album-71711391_276277792
# считаю, что это еще какой мем. Если вы так не считаете, то знайте,
# мемы у всех разные


async def main():
    async with async_session() as session:
        rep = MemRepository(session)
        for link in links:
            obj_in = MemInCreatePydantic(
                link=link
            )
            await rep.create(obj_in)


asyncio.run(main())
