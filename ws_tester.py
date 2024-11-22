import aiohttp
import asyncio


async def websocket_client():
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://localhost:8000/scan/",
            json={"targets": ["127.0.0.1"]},
        ) as response:
            data = await response.json()
            print(data)
            task_id = data["task_id"]
        async with session.ws_connect(
            f"ws://localhost:8000/scan/{task_id}",
        ) as websocket:
            async for message in websocket:
                print(f"Received: {message}")


asyncio.run(websocket_client())
