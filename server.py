#!/usr/bin/env python3

import asyncio
import websockets
import json

traffic_lights_state = {
  'A1': 0,
  'A2': 0,
  'A3': 0,
  'A4': 0,

  'AB1': 0,
  'AB2': 0,

  'B1': 0,
  'B2': 0,
  'B3': 0,
  'B4': 0,

  'BB1': 0,

  'C1': 0,
  'C2': 0,
  'C3': 0,

  'D1': 0,
  'D2': 0,
  'D3': 0,

  'E1': 0,
  'E2': 0,

  'EV1': 0,
  'EV2': 0,
  'EV3': 0,
  'EV4': 0,

  'FV1': 0,
  'FV2': 0,
  'FV3': 0,
  'FV4': 0,

  'FF1': 0,
  'FF2': 0,

  'GV1': 0,
  'GV2': 0,
  'GV3': 0,
  'GV4': 0,

  'GF1': 0,
  'GF2': 0,
}


async def index(websocket, path):
  async for message in websocket:
    data = json.loads(message)

    print(f"< {data}")

    payload = json.dumps(traffic_lights_state)
    await websocket.send(payload)

start_server = websockets.serve(index, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()