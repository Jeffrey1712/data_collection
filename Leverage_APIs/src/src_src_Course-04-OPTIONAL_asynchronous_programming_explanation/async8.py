import asyncio
import time
import logging
import requests
import json
from tornado.httpclient import AsyncHTTPClient

logger = logging.getLogger(__name__)

#response1 = requests.get("https://api.teleport.org/api/cities/?search=San%20Francisco")

async def API_call(query, client):
    # API down
    # url = f"https://api.teleport.org/api/cities/?search={city}"
    url = f"https://api.openaq.org/v2/countries/{query}"
    print(url)
    r = await client.fetch(url)
    return json.loads(r.body.decode())

async def search(cities):
    client = AsyncHTTPClient()
    logger.info("Starting query...")
    start = time.time()
    tasks = [asyncio.create_task(API_call(str(city), client)) for city in cities]
    result =  await asyncio.gather(*tasks)
    end = time.time()
    elapsed = str(end - start)
    logger.info("The process took {} seconds".format(elapsed))
    return result