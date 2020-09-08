from sheets import *


def update_sheet():
    clan = requests.get('https://api.clashofclans.com/v1/clans/' + CLAN_TAG, headers=headers).json()
    member_list = clan['memberList']
    update_members(member_list)
    print(get_time() + ' - Members Updated.')
    print(get_time() + ' - Updating Analytics')
    update_analytics(member_list)
    print(get_time() + ' - Analytics Updated')

    current_war = requests.get('https://api.clashofclans.com/v1/clans/' + CLAN_TAG + '/currentwar', headers=headers).json()

    update_current(current_war)    #

    print(get_time() + ' - War Updated.')

    update_league()

    update_metrics(data)  # Update Aggregate data: AVG Stars, War Eff., Star Eff...
    update_league_metrics()
    #


update_sheet()


