import ezsheets
import queue
from copy import deepcopy
from funcs import get_time
import requests
from funcs import *
from metrics import *

from credentials import *

print(get_time() + ' - Program Start.')

CLAN_TAG = '%23P02CUUUU'

ss = get_spreadsheet()

# variable assignment to sheets
data = ss[0]
analytics = ss[1]

print(get_time() + ' - ' + data.title + " opened.")


def search(list, key):
    try:
        return list.index(key)
    except ValueError:
        print('\n*********\n' + str(key) + ' not found' + '\n*********\n')
        return -2


def update_members(member_list):
    print(get_time() + ' - Members Start Updating')
    dataHeaderRow = data.getRow(3)

    player_info = {
        'tag': {
            'column': data.getColumn(search(dataHeaderRow, 'Tags') + 1),
            'number': search(dataHeaderRow, 'Tags') + 1,
            'changed': False
        }
    }
    player_data = {
        'name': {
            'column': data.getColumn(search(dataHeaderRow, 'Name') + 1),
            'number': search(dataHeaderRow, 'Name') + 1,
            'changed': False
        },
        'donations': {
            'column': data.getColumn(search(dataHeaderRow, 'Given') + 1),
            'number': search(dataHeaderRow, 'Given') + 1,
            'changed': False
        },
        'donationsReceived': {
            'column': data.getColumn(search(dataHeaderRow, 'Received') + 1),
            'number': search(dataHeaderRow, 'Received') + 1,
            'changed': False
        },
        'trophies': {
            'column': ['', '', 'Trophies'] + ([0] * (data.rowCount - 3)),
            'number': search(dataHeaderRow, 'Trophies') + 1,
            'changed': True
        },
    }

    names_added = []

    for member in member_list:
        member['name'] = member['name'].replace('==', '::')

        player_index = search(player_info['tag']['column'], member['tag'])

        if player_index < 0:  # not found
            player_info['tag']['column'].append(member['tag'])
            names_added.append(member['name'])

            player_index = data.rowCount
            data.rowCount += 1

        for k, v in player_data.items():
            if player_index > len(v['column']) - 1:
                v['column'].append(member[k])
            else:
                v['column'][player_index] = member[k]

    if len(names_added) != 0:
        print(get_time() + ' - Member(s) added to sheet: ' + str(names_added))

    player_data['name']['column'][1] = 'Updated ' + simple_time()

    for k, v in {**player_data, **player_info}.items():
        data.updateColumn(v['number'], v['column'])


def update_current(current_war):
    if current_war['state'] == 'notInWar':
        return

    war_id_row = data.getRow(2)
    header_row = data.getRow(3)

    info = {
        'tags': {'column': data.getColumn(search(header_row, 'Tags') + 1),
                 'number': search(header_row, 'Tags') + 1,
                 'changed': False
                 }
    }
    column = {
        'attack 1': {'column': [],
                     'number': -1,
                     },
        'pos 1': {'column': [],
                  'number': -1,
                  },
        'attack 2': {'column': [],
                     'number': -1,
                     },
        'pos 2': {'column': [],
                  'number': -1,
                  },
    }
    # 1) attempt to find current war identifier within sheet
    try:
        war_column_number = war_id_row.index(current_war['endTime'])

        for i in range(1, 3):  # 1, 2
            war_column_number += 1
            column['attack ' + str(i)]['number'] = war_column_number
            column['attack ' + str(i)]['column'] = data.getColumn(war_column_number)

            war_column_number += 1
            column['pos ' + str(i)]['number'] = war_column_number
            column['pos ' + str(i)]['column'] = data.getColumn(war_column_number)

    except ValueError:  # war not found

        # add rows and load headers to columns

        data.columnCount += 4
        war_column_number = data.columnCount - 4
        for i in range(1, 3):  # 1, 2
            war_column_number += 1
            column['attack ' + str(i)]['number'] = war_column_number
            column['attack ' + str(i)]['column'] = data.getColumn(war_column_number)

            war_column_number += 1
            column['pos ' + str(i)]['number'] = war_column_number
            column['pos ' + str(i)]['column'] = data.getColumn(war_column_number)

            pos_header = ['', '', 'Pos']
            attack_header = []
            if i == 1:
                end = current_war['endTime']
                attack_header = ['War ' + str(end[4:6] + '/' + end[6:8] + '/' + end[2:4]), current_war['endTime'], 'Attack 1']

            elif i == 2:
                attack_header = ['', '', 'Attack 2']

            for num, item in enumerate(attack_header):
                column['attack ' + str(i)]['column'][num] = item

            for num, item in enumerate(pos_header):
                column['pos ' + str(i)]['column'][num] = item

    for member in current_war['clan']['members']:
        try:
            index = info['tags']['column'].index(member['tag'])

            if current_war['state'] == 'warEnded':
                stars = ['-', '-']
            else:
                stars = ['--', '--']

            star_pos = ['', '']

            if 'attacks' in member:
                for attack_index, attack in enumerate(member['attacks']):
                    stars[attack_index] = attack['stars']

                    for enemy_player in current_war['opponent']['members']:
                        if enemy_player['tag'] == attack['defenderTag']:
                            diff = member['mapPosition'] - enemy_player['mapPosition']

                            if diff >= 0:
                                star_pos[attack_index] = '^' + str(diff)
                            else:
                                star_pos[attack_index] = 'v' + str(diff * -1)

            for attack_index, star in enumerate(stars):
                column['attack ' + str(attack_index + 1)]['column'][index] = star
            for attack_index, pos in enumerate(star_pos):
                column['pos ' + str(attack_index + 1)]['column'][index] = pos

        except ValueError:
            pass

    for k, v in column.items():
        data.updateColumn(v['number'], v['column'])


def update_league():
    print(get_time() + ' - Start update_league()')
    league_group = requests.get('https://api.clashofclans.com/v1/clans/' + CLAN_TAG + '/currentwar/leaguegroup',
                                headers=headers).json()

    if 'reason' in league_group:  # no api information
        return

    update_league_clans(league_group)

    war_list = queue.Queue()
    for day_num in range(1, 8):
        day = league_group['rounds'][day_num - 1]
        for match_up in day['warTags']:
            if match_up != '#0':
                match_tag = match_up.replace('#', '%23')
                league_war = requests.get(
                    'https://api.clashofclans.com/v1/clanwarleagues/wars/' + match_tag,
                    headers=headers
                ).json()

                league_war['match_tag'] = match_tag
                league_war['day'] = day_num

                update_league_stars(league_war)
                for (k, clan) in league_war.items():
                    if k == 'clan' or k == 'opponent':
                        if clan['tag'].replace('#', '%23') == CLAN_TAG:
                            if league_war['state'] != 'preparation':

                                clan['battleTag'] = match_tag
                                clan['state'] = league_war['state']

                                war_list.put(clan)
                                if war_list.qsize() > 3:
                                    war_list.get()

    player_tags = data.getColumn(2)
    header = data.getRow(2)

    count = 0
    while not war_list.empty():
        war = war_list.get()

        try:
            current_war_column = header.index(war['battleTag']) + 1
            attack_list = data.getColumn(current_war_column)
        except ValueError:
            print('War being added')
            data.columnCount += 1
            current_war_column = data.columnCount
            attack_list = data.getColumn(current_war_column)

            if count == 0:
                attack_list[0] = 'League ' + league_group['season']
            attack_list[1] = war['battleTag']
            attack_list[2] = 'Day {0}'.format(count + 1)

        for member in war['members']:
            try:
                player_index = player_tags.index(member['tag'])

                if 'attacks' in member:
                    for attack in member['attacks']:
                        attack_list[player_index] = attack['stars']
                else:
                    if war['state'] == 'warEnded':
                        attack_list[player_index] = '-'
                    else:
                        attack_list[player_index] = '--'

            except ValueError:
                pass

        data.updateColumn(current_war_column, attack_list)
        count += 1

    print(get_time() + ' - League update complete')


def update_league_clans(league_group):
    # this creates CWL sheet for each clan
    # adds roster members and info, updates attacks, and predicts upcoming lineup

    # should only update members if needed (even if deleted on sheet)
    for clan in league_group['clans']:
        sheet_title = 'CWL - ' + clan['name']
        if sheet_title not in ss.sheetTitles:
            print(get_time() + ' - Adding ' + clan['name'] + ' member data to spreadsheet')
            ss.createSheet(sheet_title, len(ss.sheetTitles))
            sheet = ss[len(ss.sheetTitles) - 1]
            columns = ['Name', 'Tags', 'Pos', 'Town Hall', 'Stars For']
            sheet.columnCount = len(columns)
            sheet.rowCount = 3
            sheet.updateRow(1, [clan['name'], ''])
            sheet.updateRow(2, ['Players'])
            sheet.updateRow(3, columns)

        for sheet in ss:
            if sheet.title == sheet_title:
                header_row = sheet.getRow(3)

                column_list = {'name': {'column': sheet.getColumn(search(header_row, 'Name') + 1),
                                        'number': search(header_row, 'Name') + 1,
                                        'changed': False
                                        },
                               'tag': {'column': sheet.getColumn(search(header_row, 'Tags') + 1),
                                       'number': search(header_row, 'Tags') + 1,
                                       'changed': False
                                       },
                               'townHallLevel': {'column': sheet.getColumn(search(header_row, 'Town Hall') + 1),
                                                 'number': search(header_row, 'Town Hall') + 1,
                                                 'changed': False
                                                 }
                               }

                for member in clan['members']:
                    member_index = search(column_list['tag']['column'], member['tag'])
                    if member_index < 0:
                        for k, v in column_list.items():
                            v['column'].append(member[k])
                            v['changed'] = True
                    else:
                        for k, v in column_list.items():
                            if v['column'][member_index] != member[k]:
                                v['changed'] = True
                                v['column'][member_index] = member[k]

                for k, v in column_list.items():
                    if v['changed']:
                        sheet.updateColumn(v['number'], v['column'])


def update_league_stars(league_war):
    # league war has attack information for 2 clans
    for k, clan in league_war.items():
        if k == 'clan' or k == 'opponent':
            for num, title in enumerate(ss.sheetTitles):
                if title == 'CWL - ' + clan['name']:
                    sheet = ss[num]

                    match_column_start = search(sheet.getRow(2), league_war['match_tag']) + 1
                    if match_column_start < 0:
                        sheet.columnCount += 1
                        match_column_start = sheet.columnCount

                    pos_column_start = search(sheet.getRow(3), 'Pos') + 1

                    info = {'event': {'row': sheet.getRow(1),
                                      'number': 1,
                                      'changed': False
                                      },
                            'tag': {'column': sheet.getColumn(2),
                                    'number': 2,
                                    'changed': False
                                    },
                            }

                    column_list = {'position': {'column': sheet.getColumn(pos_column_start),
                                                'number': pos_column_start,
                                                'changed': False
                                                },
                                   'attack': {'column': sheet.getColumn(match_column_start),
                                              'number': match_column_start,
                                              'changed': False
                                              }
                                   }

                    if league_war['state'] == 'preparation':
                        column_list['attack']['column'] = [''] * sheet.rowCount
                        column_list['position']['column'] = [''] * sheet.rowCount
                        column_list['position']['column'][2] = 'Pos'
                        column_list['attack']['changed'] = True
                        column_list['position']['changed'] = True

                    leagueDate = 'League ' + league_war['startTime'][4:6] + '-' + league_war['startTime'][0:4]
                    if search(info['event']['row'], leagueDate) < 0:
                        column_list['attack']['column'][0] = leagueDate

                    column_list['attack']['column'][1] = league_war['match_tag']
                    column_list['attack']['column'][2] = 'Day ' + str(league_war['day'])

                    for member in clan['members']:
                        player_index = search(info['tag']['column'], member['tag'])
                        column_list['position']['column'][player_index] = member['mapPosition']
                        if 'attacks' in member:
                            for attack in member['attacks']:
                                if player_index >= 0:
                                    if column_list['attack']['column'][player_index] != str(attack['stars']):
                                        column_list['attack']['column'][player_index] = attack['stars']
                                        column_list['attack']['changed'] = True
                        else:
                            if league_war['state'] == 'warEnded':
                                symbol = '-'
                            else:
                                symbol = '--'

                            if column_list['attack']['column'][player_index] != symbol:
                                column_list['attack']['column'][player_index] = symbol
                                column_list['attack']['changed'] = True

                    for k, v in column_list.items():
                        if v['changed']:
                            sheet.updateColumn(v['number'], v['column'])

                            if k == 'attack':
                                print(get_time() + ' - Updating {0} Day {1}'.format(clan['name'], league_war['day']))


def update_league_metrics():
    for sheet in ss:
        if sheet.title.find('CWL') >= 0:
            column_names = sheet.getRow(3)

            info = {
                'header': {'row': sheet.getRow(1),
                           'number': 1,
                           'changed': False
                           },
                'tags': {'column': sheet.getColumn(2),
                         'number': 2,
                         'changed': False
                         }
            }

            column_list = {
                'stars': {'column': sheet.getColumn(search(column_names, 'Stars For') + 1),
                          'number': search(column_names, 'Stars For') + 1,
                          'changed': False
                          }

            }

            for i, event in enumerate(reversed(info['header']['row'])):
                if event.find('League') >= 0:
                    # print(info['header']['row'][0], event)
                    for row, player_tag in enumerate(info['tags']['column']):
                        if player_tag.find('#') >= 0:
                            player_row = sheet.getRow(row + 1)
                            start_index = len(info['header']['row']) - i - 1

                            initial_value = str(column_list['stars']['column'][row])
                            if str(get_sum_stars(player_row, start_index)) != initial_value:
                                column_list['stars']['column'][row] = get_sum_stars(player_row, start_index)
                                column_list['stars']['changed'] = True

                    for k, v in column_list.items():
                        if v['changed']:
                            sheet.updateColumn(v['number'], v['column'])
                            print(get_time() + ' Updating ' + info['header']['row'][0] + ' ' + k + ' metrics.')
                    break


def update_analytics(member_list):

    tagColumn = ['Tag']
    nameColumn = ['Name']
    dataHeaderRow = data.getRow(3)
    analyticsHeaderRow = analytics.getRow(1)

    analyticsHeroColumns = {
        'Barbarian King': {'column': ['King'],
                           'number': search(analyticsHeaderRow, 'King') + 1},
        'Archer Queen': {'column': ['Queen'],
                         'number': search(analyticsHeaderRow, 'Queen') + 1},
        'Grand Warden': {'column': ['Warden'],
                         'number': search(analyticsHeaderRow, 'Warden') + 1},
        'Royal Champion': {'column': ['Champion'],
                           'number': search(analyticsHeaderRow, 'Champion') + 1},
    }
    dataColumns = {
        'tag': {
            'column': data.getColumn(search(dataHeaderRow, 'Tags') + 1),
            'number': search(dataHeaderRow, 'Tags') + 1
        },
        'warStars': {
            'column': data.getColumn(search(dataHeaderRow, 'War Stars') + 1),
            'number': search(dataHeaderRow, 'War Stars') + 1
        },
        'townHallLevel': {
            'column': data.getColumn(search(dataHeaderRow, 'TH') + 1),
            'number': search(dataHeaderRow, 'TH') + 1
        }
    }

    for member in member_list:
        member['name'] = member['name'].replace('==', '::')
        nameColumn.append(member['name'])
        tagColumn.append(member['tag'])

        player_stats = requests.get('https://api.clashofclans.com/v1/players/' + member['tag'].replace('#', '%23'),
                                    headers=headers).json()

        playerHeroes = [hero for hero in player_stats['heroes'] if hero['name'] != 'Battle Machine']
        for i, (k, v) in enumerate(analyticsHeroColumns.items()):
            if i < len(playerHeroes):
                # print([hero['level'] for hero in playerHeroes if hero['name'] == k])
                v['column'].append([hero['level'] for hero in playerHeroes if hero['name'] == k][0])
            else:
                v['column'].append('#UND')

        player_index = search(dataColumns['tag']['column'], member['tag'])
        for k, v in dataColumns.items():
            if k != 'tag':
                v['column'][player_index] = player_stats[k]

    analytics.rowCount = len(tagColumn)
    analyticsHeroColumns['Tag'] = {'column': tagColumn, 'number': 2}
    analyticsHeroColumns['Name'] = {'column': nameColumn, 'number': 1}

    for k, v in analyticsHeroColumns.items():
        analytics.updateColumn(v['number'], v['column'])
    for k, v in dataColumns.items():
        data.updateColumn(v['number'], v['column'])