from src.connection_manager import run_server
import asyncio


async def main():
    host = '10.0.0.171'
    # host = '192.168.50.223'  # choose_host()
    await run_server(host)


if __name__ == "__main__":
    asyncio.run(main())
