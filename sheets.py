import ezsheets
from funcs import get_time

ss = ezsheets.Spreadsheet('1b39nbYf6Z_EiK8WlTkgND9KMRqXX72AbdJ0ngrlq1Ag')
data = ss[0] # get the first sheet in the spreadsheet
CLAN_TAG = '%23P02CUUUU'

print(get_time() + ' - ' + ss.title + " opened.")


def reset_trophies():
    #troph_index = data.getRow(2).index('Trophies') + 1
    trophies = data.getColumn(3)        # list of member trophies
    for i in range(2, len(trophies)):   # change trophy list
        trophies[i] = 0

    data.updateColumn(3, trophies)      # update sheet with changed trophies

def update_members(member_list):
    player_column = data.getColumn('A')     # sheet column of player tags
    count = 0
    for member in member_list:
        count = count + 1
        print('\tUpdating members: ' + str(int((count / len(member_list) * 100))) + '%\r', end='', flush=True)
        try:
            if member['name'] == '==d1ego==':
                member['name'] = '::diego::'
            row = player_column.index(member['name']) + 1      # row starts at 1, list starts at zero

            # exception not thrown, update player

            #print(get_time() + ' - Updating ' + member['name'] + ' in row: ' + str(row))
            player_tuple = data.getRow(row)
            # tuple is the entire row as list

            # issue: this will overwrite function line with return data (ex: sum stars )

            # change the list
            player_tuple[1] = member['tag']
            player_tuple[2] = member['trophies']
            player_tuple[3] = member['donations']
            player_tuple[4] = member['donationsReceived']
            player_tuple[6] = member['role']

            data.updateRow(row, player_tuple)     # replaces the entire row with list
        except ValueError:
            print(get_time() + ' - ' + member['name'] + ' added to Sheet.')

            data.rowCount = data.rowCount + 1   # make a new row

            # fill with player information
            #  column:          A                  B                    C                       D                E              F        G
            new_tuple = [ member['name'], member['tag'],  member['trophies'], member['donations'], member['donationsReceived'], '', member['role']]
            data.updateRow(data.rowCount, new_tuple)


def update_wars(current_war):
    tags = data.getColumn(2)            # look up player in sheet
    war_row = data.getRow(1)            # used when wanting to search for war index identifier (war['endTime] )


    try:
        war_index = war_row.index(current_war['endTime'])

        # war end found, get columns for attacks
        attack_1 = data.getColumn(war_index)
        attack_2 = data.getColumn(war_index + 1)
    except ValueError:
        print(get_time() + ' - Current war added.')
        # 1: make room in spreadsheet
        for i in range(1, 3):
            data.columnCount = data.columnCount + 1
            if i == 1:
                attack_1 = data.getColumn(data.columnCount)
            else:
                attack_2 = data.getColumn(data.columnCount)

        # Add attributes to top rows
        end = current_war['endTime']
        attack_2[0] = end
        attack_1[0] = 'War '+ str(end[4:6] + '/' + end[6:8] + '/' + end[2:4])

        attack_1[1] = 'Attack 1'
        attack_2[1] = 'Attack 2'

    # war columns identified, now gathers attack data

    clan = current_war['clan']      # our clan
    for member in clan['members']:
        try:
            index = tags.index(member['tag'])
            stars = ['-', '-']
            if 'attacks' in member:
                count = 0
                for attack in member['attacks']:
                    stars[count] = attack['stars']
                    count = count + 1

            attack_1[index] = stars[0]
            attack_2[index] = stars[1]

        except ValueError:
            pass

    # write list columns to sheet
    data.updateColumn(data.columnCount, attack_2)
    data.updateColumn(data.columnCount - 1, attack_1)






















