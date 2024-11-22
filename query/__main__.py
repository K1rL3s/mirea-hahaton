import asyncio

from .app import create_app

if __name__ == "__main__":

    async def main() -> None:
        app = await create_app()
        await app.run()

    asyncio.run(main())
