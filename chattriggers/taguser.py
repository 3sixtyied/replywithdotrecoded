import asyncio
import os

import allowuselimited
import chattrigger
from persistentstorage import PersistentStorage


class TagUser(chattrigger.ChatTrigger):

    async def run(self, message, trigger, client):

        if not allowuselimited.allowuselimited(message.author.id,
                                               client):  # 2020-05-07 realized this would be a good idea for this
            return

        n = message.content.split(" ")
        # persontotag = message.mentions[0]
        persontotag = n[1]  # to allow for role tagging
        numberoftimes = int(n[2])
        tomessage = " ".join(n[3:])
        # print(f"n = {n}, len(n) = {len(n)}") # debugging
        taguserlimitchannelid = int(os.environ.get("TAG_USER_LIMIT_CHANNEL_ID"))
        limitreader = PersistentStorage("Limit Reader", taguserlimitchannelid, client, ".")
        limit = int((await limitreader.read())[0])
        # print(f"{limit}, {type(limit)}. {numberoftimes}, {type(numberoftimes)}") # debugging
        if not message.author.id == int(os.environ.get("OWNER_ID")):
            if numberoftimes > limit:
                await message.channel.send(f"Command Aborted! n({numberoftimes}) is larger than(>) limit({limit})!")
                return

        for i in range(numberoftimes):
            await message.channel.send(f"{persontotag}, {tomessage} | {i + 1}/{numberoftimes}")
            await asyncio.sleep(2)
