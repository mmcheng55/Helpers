from .Commander import Commander
import asyncio


class TCPEcho:
    def __init__(self, loop: asyncio.AbstractEventLoop = None):
        self.loop = loop if loop is not None else asyncio.get_event_loop()
        self.loop.create_task(asyncio.start_server(self.handle_client, 'localhost', 15555))
        self.Command = Commander()

    def run(self):
        self.loop.run_forever()

    async def handle_client(self, reader, writer):
        request = None
        while request != 'quit' or request != 'exit':
            request = (await reader.read(255)).decode('utf8')
            response = str((await self.Command.run_async(request)).encode("utf-8")) + '\n'
            writer.write(response.encode('utf8'))
            await writer.drain()
        writer.close()