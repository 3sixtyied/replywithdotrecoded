import asyncio
import os
import time

import autoaction
from persistentstorage import PersistentStorage


class PUSlowMode(autoaction.AutoAction):

    async def run(self, message, client):
        slowmodelistid = int(os.environ.get("SLOWMODELIST"))
        slowmodetimerid = int(os.environ.get("SLOWMODETIMER"))
        slowmodelistreader = PersistentStorage("Slow Mode List Reader", slowmodelistid, client, ".")
        slowmodetimerreader = PersistentStorage("Slow Mode Time Reader", slowmodetimerid, client, ".")

        mutedroleid = int(os.environ.get("MUTED_ROLE"))

        sml = await slowmodelistreader.read()
        smla = []

        smt = await slowmodetimerreader.read()

        # print(sml) # <- debugging stuff
        # print(smt)

        for i in sml:  # makes int oone array
            # print(i)
            # print(i.split(","))
            # print(smt)
            smla.append(i.split(","))

        # print(smla) # EVERYUTHING COMBINES

        for ic, i in enumerate(smla):
            # print(i)
            if i == None:  # avoid errors? not sure if to deprecate
                continue
            # print(i[0])
            # print(message.author)
            if message.author.id == int(i[0]):  # check if user is in slowmodelist
                # print(True)
                currenttime = int(time.time())
                try:  # if there is previous message time
                    print(smt[ic])
                    print(ic)
                    print(smt)
                    lasttime = int(smt[ic])
                # print(currenttime)
                # print(lasttime)
                except:  # if there isnt previous message time
                    towrite = ""
                    for jc, j in enumerate(smt):
                        if jc == ic:
                            towrite += str(currenttime) + "."
                        else:
                            towrite += smt[jc] + "."
                    # print(towrite)
                    towrite = towrite[:-1]
                    # print(51)
                    return False

                if currenttime - lasttime >= int(i[1]):  # check if message delay has passed
                    towrite = ""
                    for jc, j in enumerate(smt):
                        if jc == ic:
                            towrite += str(currenttime) + "."
                        else:
                            towrite += smt[jc] + "."
                    towrite = towrite[:-1]
                    towrite = "." + towrite
                    await slowmodetimerreader.write(towrite)  # update lastmessagetime
                    # print(62) # for debugging

                    await message.author.add_roles(message.guild.get_role(mutedroleid))

                    await asyncio.sleep(int(i[1]))

                    await message.author.remove_roles(message.guild.get_role(mutedroleid))
                    return False

                else:  # deprecated, shouldnt ever be triggered due to the muted role
                    try:
                        await message.delete()  # enforce slowmode
                    except:  # if bot is in server in which it doesnt have perms (example: direct messages)
                        # print("failed to delete")
                        return False
                    # print(67)
                    return True
    # print(False)

# print("do something")
