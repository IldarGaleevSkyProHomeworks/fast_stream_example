
from faststream import FastStream
from faststream.redis import RedisBroker

broker = RedisBroker("redis://localhost:6379")

app = FastStream(broker)


@broker.subscriber("service1") # слушаем сообщения из канала "service1"
@broker.publisher("service2") # результат отправляем в канал "service2"
async def base_handler(body):
    print(f"received: {body}")
    return f"service1 accept message: {body}"

# запуск сервиса в терминале:
# faststream run service1:app