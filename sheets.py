import ezsheets
from funcs import get_time
import time

ss = ezsheets.Spreadsheet('1b39nbYf6Z_EiK8WlTkgND9KMRqXX72AbdJ0ngrlq1Ag')
data = ss[0] # get the first sheet in the spreadsheet

print(get_time() + ' - ' + ss.title + " opened.")


def reset_trophies():
    trophies = data.getColumn('B')        # list of member trophies
    for i in range(2, len(trophies)):   # change trophy list
        trophies[i] = 0

    data.updateColumn(2, trophies)      # update sheet with changed trophies

def update_members(member_list):
    player_column = data.getColumn('A')     # sheet column of player tags
    for member in member_list:
        try:
            if member['name'] == '==d1ego==':
                member['name'] = '::diego::'
            index = player_column.index(member['name']) + 1     # list start at zero, row/col start at 1

            # exception not thrown, update player

            print(get_time() + ' - Updating ' + member['name'] + ' in row: ' + str(index))
            player_tuple = data.getRow(index)       # get entire row as list

            # issue: this will overwrite function line with return data (ex: sum stars )

            # change the list
            player_tuple[1] = member['trophies']
            player_tuple[2] = member['donations']
            player_tuple[3] = member['donationsReceived']
            player_tuple[5] = member['role']

            data.updateRow(index, player_tuple) # replaces the entire row
        except ValueError:
            print(get_time() + ' - ' + member['name'] + ' not found')

            data.rowCount = data.rowCount + 1   # make a new row

            # fill with player information
            #  column:          A                  B                    C                       D                E    F
            new_tuple = [ member['name'], member['trophies'], member['donations'], member['donationsReceived'], '', member['role']]
            data.updateRow(data.rowCount, new_tuple)

