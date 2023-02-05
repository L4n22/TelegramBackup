from telethon import TelegramClient
from telethon import types
import asyncio
import tqdm
import time

class TelegramBackup:
    def __init__(self, session_name, api_id, api_hash):
        self.api_id = api_id
        self.api_hash = api_hash
        self.session_name = session_name
        self.client = None
        self.src_entity = None
        self.dst_entity = None
        self.filtered_messages = []


    async def start_client(self):
        self.client = TelegramClient(
            self.session_name, 
            self.api_id,
            self.api_hash)
        
        await self.client.start()


    async def stop_client(self):
        await self.client.disconnect()


    async def set_src_entity(self, entity):
        self.src_entity = await self.client.get_input_entity(entity)
        

    async def set_dst_entity(self, entity):
        self.dst_entity = await self.client.get_input_entity(entity)
  

    def __get_src_entity_messages(self):
        return self.client.iter_messages(
            self.src_entity,
            reverse=True,
            limit=None,
            offset_date=None)
    

    async def __filter_messages(self):
        messages = self.__get_src_entity_messages()
        async for message in messages:
            if isinstance(message, types.Message) \
                and isinstance(message.media,
                    (types.MessageMediaPhoto,
                     types.MessageMediaWebPage, 
                    types.MessageMediaDocument)):
                self.filtered_messages.append(message)


    async def send_messages(self):
        await self.__filter_messages()
        for i in tqdm.tqdm(range(len(self.filtered_messages))):
            await self.client.send_message(self.dst_entity, self.filtered_messages[i])
            time.sleep(3)


    async def __aenter__(self):
        await self.start_client()


    async def __aexit__(self, exc_type, exc, tb):
        await self.stop_client()


async def main():
    #python3.10.exe -m pip install telethon
    #https://my.telegram.org/auth -> API_ID & API_HASH

    telebackup = TelegramBackup(
        session_name="example", 
        api_id=0,
        api_hash="")
    
    SRC_ENTITY = "https://t.me/+T3EXAMPLE1"
    DST_ENTITY = "https://t.me/+T3EXAMPLE2"
    async with telebackup:
        await telebackup.set_src_entity(SRC_ENTITY)
        await telebackup.set_dst_entity(DST_ENTITY)
        await telebackup.send_messages()


if __name__ == "__main__":
    asyncio.run(main())
