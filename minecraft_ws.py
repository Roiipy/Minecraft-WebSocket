import asyncio
import websockets
import json
from uuid import uuid4


async def running_ws(websocket, path):
    print('接続完了')

    await websocket.send(
        json.dumps({
            "header": {
                "version": 1,
                "requestId": str(uuid4()),
                "messageType": "commandRequest",
                "messagePurpose": "subscribe"
            },
            "body": {
                "eventName": "PlayerMessage"
            },
        }))

    try:
        async for msg in websocket:
            msg = json.loads(msg)
            try:
                if msg['body']['properties']['Message']:
                    print(f"<{msg['body']['properties']['Sender']}> {msg['body']['properties']['Message']}")
                    if msg['body']['properties']['Message'].startswith("!run:"):
                        await websocket.send(
                            json.dumps({
                                "body": {
                                    "origin": {
                                        "type": "player"
                                    },
                                    "commandLine": msg['body']['properties']['Message'][5:],
                                    "version": 1
                                },
                                "header": {
                                    "requestId": str(uuid4()),
                                    "messagePurpose": "commandRequest",
                                    "version": 1,
                                    "messageType": "commandRequest"
                                }
                            }))
            except KeyError:
                pass
    except websockets.exceptions.ConnectionClosedError:
        print('接続が切断されました。')


print('/connect localhost:7000 を実行してください。')

asyncio.get_event_loop().run_until_complete(
    websockets.serve(running_ws, host="localhost", port=7000))
asyncio.get_event_loop().run_forever()
