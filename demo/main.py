import asyncio
import aioredis
import time

from aiohttp import web



async def handler(request):
    # session = await get_session(request)

    return web.Response(text='hello')


async def make_redis_pool():
    redis_address = ('127.0.0.1', '6380')
    return await aioredis.create_redis_pool(redis_address, timeout=1)


def make_app():
    loop = asyncio.get_event_loop()
    redis_pool = loop.run_until_complete(make_redis_pool())


    async def dispose_redis_pool(app):
        redis_pool.close()
        await redis_pool.wait_closed()

    app = web.Application()

    app.on_cleanup.append(dispose_redis_pool)
    app.router.add_get('/', handler)
    return app


web.run_app(make_app())