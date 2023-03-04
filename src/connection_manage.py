import asyncio


async def conn_to_controller() -> None:
    reader, writer = await asyncio.open_connection('127.0.0.1', 8082)

    writer.write(b'{"cmd":"connecting,"name_scanner":"scanner01"}')
    await writer.drain()

    while True:
        try:
            data = await reader.read(1536)

            if data:
                pass
            elif not data:
                print('Connection is closed')
                break

            print(data.decode())

        finally:
            writer.write(b'{"cmd":"closing"}')
            await writer.drain()
            writer.close()
            await writer.wait_closed()
