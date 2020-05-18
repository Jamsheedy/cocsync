import coc
from funcs import get_time

CLAN_TAG = "#P02CUUUU"
client = coc.login('djamsheedy99@gmail.com', 'Mundodeano1#', client=coc.EventsClient)

@client.event
async def on_clan_member_donation(old_donation, new_donations, player):
    difference = new_donations - old_donation
    print(get_time() + ' - {0.name} ({0.tag}) just donated {1} troop space'.format(player, difference))

@client.event
async def on_clan_member_join(member, clan):
    print( get_time() + ' - {0.name} ({0.tag}) just joined clan {1.name} ({1.tag}).'.format(member, clan))

@client.event
async def on_clan_member_leave(member, clan):
    print( get_time() + ' - {0.name} ({0.tag}) just left clan {1.name} ({1.tag}).'.format(member, clan))

@client.event
async def on_clan_member_trophies_change(old_trophies, new_trophies, player):
    print( get_time() + ' - {0.name} ({0.tag}) went from {1} to {2} trophies.'.format(player, old_trophies, new_trophies))


print( get_time() + " - Start:")
client.add_clan_update(CLAN_TAG, retry_interval=30)  # check every 30 seconds
client.run_forever()



