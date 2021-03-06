from aiohttp import web, WSMsgType
import os
import asyncio
from google.cloud import pubsub_v1

topic = os.getenv('GOOGLE_CLOUD_PUBSUB_TOPIC')
subscription = os.getenv('GOOGLE_CLOUD_PUBSUB_SUBSCRIPTION')
project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
last_message = 'NO_LAST_DATA_YET!'
routes = web.RouteTableDef()

@routes.get('/ws')
async def websocket_handler(request):
    print('Websocket connection starting')
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    request.app['websockets'].add(ws)
    print('Websocket connection ready')

    async for msg in ws:
        if msg.type == WSMsgType.TEXT and msg.data == 'close':
            await ws.close()

    print('Websocket connection closed')
    return ws

@routes.get('/last')
async def last(request):
    res = { 'message': request.app['data']['last_message'] }
    return web.json_response(res)

async def send_msg(websockets, message):
    for ws in websockets:
        print('Sending ' + message)
        await ws.send_json(message)

def subscribe_to_pubsub(app):
    # Subscribe to the Pub/Sub topic
    subscriber = pubsub_v1.SubscriberClient()
    topic_name = 'projects/{project_id}/topics/{topic}'.format(
        project_id=project_id,
        topic=topic
    )
    subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
        project_id=project_id,
        sub=subscription
    )

    # Define the callback for the pubsub
    def callback(message):
        strmessage = message.data.decode('utf-8')
        app['data']['last_message'] = strmessage
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(send_msg(app['websockets'], strmessage))
        message.ack()

    future = subscriber.subscribe(subscription_name, callback)

def create_app():
    # Start the websocket server
    app = web.Application()
    app.add_routes(routes)
    app.router.add_static('/', path=str('./www/'))
    app['websockets'] = set()
    # this is only for testing purposes, for a production mode, the last message should be stored
    # in a distributed cache like Redis
    app['data'] = {}
    app['data']['last_message'] = last_message
    return app

def main():
    app = create_app()
    subscribe_to_pubsub(app)
    web.run_app(app)

if __name__ == "__main__":
    main()