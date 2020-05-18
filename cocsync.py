import coc
import asyncio

CLAN_TAG = "#P02CUUUU"
client = coc.login('djamsheedy99@gmail.com', 'Mundodeano1#', client=coc.EventsClient)

@client.event
async def on_clan_member_donation(old_donation, new_donations, player):
    difference = new_donations - old_donation
    print('{0.name} ({0.tag}) just donated {1} troop space'.format(player, difference))

client.add_events(on_clan_member_donation)
print("Here")
client.add_clan_update(CLAN_TAG, retry_interval=30)  # check every 30 seconds
client.run_forever()



