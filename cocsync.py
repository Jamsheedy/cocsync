import coc
import asyncio

CLAN_TAG = "#P02CUUUU"
client = coc.login(email='djamsheedy99@gmail.com', password='Mundodeano1#', client=coc.EventsClient)
client.add_clan_update(CLAN_TAG)


print("Done!")