import coc
from funcs import get_time
from sheets import update_trophies

from sheets import *

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
    update_trophies(player, new_trophies)
    print( get_time() + ' - {0.name} ({0.tag}) went from {1} to {2} trophies.'.format(player, old_trophies, new_trophies))

@client.event
async def on_war_attack(attack, war):
    if attack.is_opponent:
        print(get_time() + ' - {0.attacker}(Opp) did {0.stars} stars on {0.defender}.'.format(attack, war))
    else:
        print(get_time() + ' - {0.attacker} did {0.stars} stars on {0.defender}(Opp).'.format(attack, war))
async def get_players():
    the_clan = await client.get_clan(tag=CLAN_TAG)
    print(type(the_clan))


print( get_time() + " - Start:")
get_players()

client.add_clan_update(CLAN_TAG, retry_interval=30)  # check every 30 seconds
client.run_forever()
# for player in the_clan.get_detailed_members(cache = True)
#     print(player.name)



