import asyncio

import requests

from backend.core.database import async_session
from backend.mem.repository import MemRepository
from backend.mem.schemas import MemInCreatePydantic

response = requests.get(
    'https://api.vk.com/method/photos.get',
    params={
        'access_token': '463f8122463f8122463f81229d464293c64463f463f81222492cbe1cde3e891a675a67a',
        'v': '5.131',
        'owner_id': '-197700721',
        'album_id': '281940823',
        'count': 100
    }
)
items = response.json()['response']['items']
links_selected = []
for item in items:
    url = list(filter(lambda x: x['width'] >= 300, item['sizes']))[0]['url']
    links_selected.append(url)


async def main():
    async with async_session() as session:
        rep = MemRepository(session)
        for link in links_selected:
            obj_in = MemInCreatePydantic(
                link=link
            )
            await rep.create(obj_in)


asyncio.run(main())
