import ezsheets
from funcs import get_time

headers = {
    'Accept': 'application/json',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImYzMTMxNzZmLWUwODEtNDVmMi1iYTlhLWM1NDRkYzhmZmNkZiIsImlhdCI6MTU4OTc3NDY1NCwic3ViIjoiZGV2ZWxvcGVyLzI3YTNlOTk5LTI4OWItYTY5ZS1hODI4LTE0OTVjYjViZjM1YyIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjguMTkuNTYuMTc5Il0sInR5cGUiOiJjbGllbnQifV19.VIpI57HHPggv0-sWfPZsCadQuNAM0SOX1UiO2FaJBbwIirlGDKMNGAKMnBkTspuxG2DRQ3jRYsuYWNGUkMo3Qg'

}
CLAN_TAG = '%23P02CUUUU'

ss = ezsheets.Spreadsheet('1b39nbYf6Z_EiK8WlTkgND9KMRqXX72AbdJ0ngrlq1Ag')
data = ss[0]  # get the first sheet in the spreadsheet

print(get_time() + ' - ' + ss.title + " opened.")


def update_members(member_list):
    reset_trophies()
    # set all trophies to zero
    # this will later result in members not in the clan anymore having zero trophies

    player_tag_column = data.getColumn('B')  # sheet column of player tags
    count = 0

    for member in member_list:
        count = count + 1
        # loading percentage displayed
        try:
            # more_member_data.append(requests.get('https://api.clashofclans.com/v1/players/' + member['tag'], headers=headers).json())

            # this gives us more detailed player data: WarStars(Overall) , Troop levels, etc
            row = player_tag_column.index(member['tag']) + 1  # row starts at 1, list starts at zero

            # clash_player_data = requests.get('https://api.clashofclans.com/v1/players/' + member['tag'], headers=headers).json()

            # exception not thrown, update player

            player_tuple = data.getRow(row)

            print('\tUpdating members: ' + str(int((count / len(member_list) * 100))) + '%' + '\r',
                  end='', flush=True)
            # tuple is the entire row as list

            if member['name'] == '==d1ego==':
                member['name'] = '::d1ego::'

            # change the list
            player_tuple[0] = member['name']
            player_tuple[2] = member['trophies']
            player_tuple[3] = member['donations']
            player_tuple[4] = member['donationsReceived']
            player_tuple[6] = member['role']

            data.updateRow(row, player_tuple)  # replaces the entire row with list
        except ValueError:

            data.rowCount = data.rowCount + 1  # make a new row

            # fill with player information
            #  column:          A                  B                    C                       D                E              F        G
            new_tuple = [member['name'], member['tag'], member['trophies'], member['donations'],
                         member['donationsReceived'], '', member['role']]
            data.updateRow(data.rowCount, new_tuple)

            print(get_time() + ' - ' + member['name'] + ' added to Sheet.')


def reset_trophies():
    # troph_index = data.getRow(2).index('Trophies') + 1
    trophies = data.getColumn(3)  # list of member trophies
    for i in range(2, len(trophies)):  # change trophy list
        trophies[i] = 0

    data.updateColumn(3, trophies)  # update sheet with changed trophies


def update_current(current_war):
    tags = data.getColumn(2)  # look up player in sheet
    war_row = data.getRow(1)  # used when wanting to search for war index identifier (war['endTime] )

    try:
        war_index = war_row.index(current_war['endTime'])  # search for war and get column num for last war

        # war end found, get columns for attacks
        attack_1 = data.getColumn(war_index)
        attack_2 = data.getColumn(war_index + 1)
    except ValueError:
        # current war not found, needs to be added to sheet
        print(get_time() + ' - Current war added.')

        # 1: make room in spreadsheet
        # need to make so this can work for war league

        for i in range(1, 3):
            data.columnCount = data.columnCount + 1
            if i == 1:
                attack_1 = data.getColumn(data.columnCount)
            else:
                attack_2 = data.getColumn(data.columnCount)

        # Add attributes to top rows
        end = current_war['endTime']
        attack_2[0] = end
        attack_1[0] = 'War ' + str(end[4:6] + '/' + end[6:8] + '/' + end[2:4])

        attack_1[1] = 'Attack 1'
        attack_2[1] = 'Attack 2'

    # war columns identified, now gathers attack data

    clan = current_war['clan']  # our clan
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

