__author__ = 'candy'

__all__ = ["mw_setup_session_middleware"]

from aiohttp import web
import json

STORAGE_KEY='mw_aio_storage'
SESSION_KEY='mw_aio_session'
COOKIE_NAME ='sessionid'

def session_middleware(storage):
    @web.middleware
    async def factory(request, handler):
        # print("in session middleware")
        # 仅检查session 是否合法，并不做产生和保存session动作
        #
        await storage.load_session(request)
        raise_response = False
        try:
            response = await handler(request)
        except web.HTTPException as exc:
            response = exc
            raise_response = True
        if raise_response:
            raise response
        return response
    return factory

class SessionRedisStorage():
    def __init__(self,redis_pool,cookie_name=COOKIE_NAME):
        self._redis =redis_pool
        self.cookie_name =cookie_name
    async def load_session(self,request):
        session = request.get(SESSION_KEY)
        if session is None:
            cookieid = request.cookies.get(self.cookie_name)
            if cookieid is not None:
                with await self._redis as conn:
                    data = await conn.get('session:%s' % str(cookieid))
                    if data is not None:
                        data = data.decode('utf-8')
                        try:
                            data = json.loads(data)
                        except ValueError:
                            data = None
                        if data is not None:
                            request[SESSION_KEY]= data
                            return data


def setup_session_middleware(app, storage):
    """Setup the library in aiohttp fashion."""
    app.middlewares.append(session_middleware(storage))

def mw_setup_session_middleware(app,redis_pool):
    storage =SessionRedisStorage(redis_pool)
    # app[STORAGE_KEY]=storage
    setup_session_middleware(app,storage)