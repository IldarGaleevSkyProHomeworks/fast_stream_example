from faststream.redis import RedisBroker
from aiohttp import web


routes = web.RouteTableDef() # роутер веб сервера
msg_broker = RedisBroker("redis://localhost:6379") # брокер сообщений на базе редиски


async def start_broker(app):
    await msg_broker.start() # запуск брокера

async def stop_broker(app):
    await msg_broker.close() # остановка брокера


@msg_broker.subscriber("service2") # подписка на сообщения из канала "service2"
async def msg_handler(body):
    print(body)


##### веб сервер ######
    
@routes.get('/')
@routes.get('/{name}')
async def handle(request): # эндпоинт веб сервера
    name = request.match_info.get('name', "Anonymous")
    
    print(f"request: {request.path}")
    
    text = "Hello, " + name
    
    await msg_broker.publish(name, channel="service1") # публикация сообщения в канал "service1"
    return web.Response(text=text) # ответ веб сервера


if __name__ == '__main__':
    app = web.Application()
    app.add_routes(routes)
    app.on_startup.append(start_broker)
    app.on_cleanup.append(stop_broker)
    web.run_app(app, host="localhost", port=8000)