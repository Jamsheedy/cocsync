from funcs import get_time


def update_metrics(sheet):
    header = sheet.getRow(3)  # row needed to look up the columns
    try:
        # use header to look up column numbers and return COLUMN number ( index + 1 )
        # column_indicies = {'AVG Stars': header.index('AVG Stars') + 1,
        #                     'War Efficiency': header.index('War Efficiency') + 1,
        #                     'Star Efficiency': header.index('Star Efficiency') + 1,
        #                    'AVG Attack Pos': header.index('AVG Attack Pos') + 1
        #                     }

        columns = {
            'AVG Stars': {},
            'War Efficiency': {},
            'Star Efficiency': {},
            'AVG Attack Pos': {}
        }

        for k, v in columns.items():
            v['number'] = header.index(k) + 1
            v['column'] = sheet.getColumn(v['number'])

        start_war = header.index('Attack 1')
    except ValueError:
        print(get_time() + ' - ERROR: Column not in sheet row 2!')
        return

    for i in range(3, sheet.rowCount):
        player_row = sheet.getRow(i + 1)  # get player row from column

        # ATTRIBUTES WE ARE STORING
        # note: we only use one api request for n attributes

        player_metrics = {
            'AVG Stars': get_avg_stars(player_row, start_war),
            'War Efficiency': get_war_efficiency(player_row, start_war),
            'Star Efficiency': get_star_efficiency(player_row, start_war),
            'AVG Attack Pos': get_avg_attack_pos(player_row, start_war)
        }

        for k, v in player_metrics.items():
            columns[k]['column'][i] = v

    for k, v in columns.items():
        sheet.updateColumn(v['number'], v['column'])

    # all metrics up to date
    print(get_time() + ' - Metrics Updated')


# function definitions for the function definitions for every metric

def get_avg_stars(y_current, start):
    star_list = []
    attack_available = False
    for i in range(start, len(y_current)):
        try:
            star = int(y_current[i])  # get the cell in player row
            if 3 >= star >= 0:
                star_list.append(star)
            # else is not a star, could be clan games, maybe decimals im not sure
        except ValueError:  # its a string, or dash, so we do nothing
            if y_current[i] == '-':
                attack_available = True

    # selective output
    if attack_available and len(star_list) == 0:
        return 0
    elif len(star_list) == 0:
        return '#UND'
    else:
        return round(sum(star_list) / len(star_list), 3)


def get_war_efficiency(y_current, start):
    attacks_used = 0
    attacks_available = 0
    for i in range(start, len(y_current)):
        try:
            star = int(y_current[i])  # get the cell in player row
            if 3 >= star >= 0:
                attacks_used += 1
                attacks_available += 1
            # else is not a star, could be clan games, maybe decimals im not sure
        except ValueError:  # its a string, need to handle missed attacks('-')
            if y_current[i] == '-':
                attacks_available += 1

    if attacks_available == 0:
        return '#UND'

    return round(attacks_used / attacks_available * 100, 2)


def get_star_efficiency(y_current, start):
    stars_earned = 0
    stars_available = 0
    for i in range(start, len(y_current)):
        try:
            star = int(y_current[i])  # get the cell in player row
            if 3 >= star >= 0:
                stars_earned += star
                stars_available += 3
            # else is not a star, could be clan games, maybe decimals im not sure
        except ValueError:  # its a string, need to handle missed attacks('-')
            if y_current[i] == '-':
                stars_available += 3

    if stars_available == 0:
        return '#UND'
    return round(stars_earned / stars_available * 100, 2)


def get_sum_stars(y_current, start):
    num_stars = 0
    for i in range(start, len(y_current)):
        try:
            star = int(y_current[i])
            if 3 >= star >= 0:
                num_stars += star
        except ValueError:
            pass

    return num_stars


def get_avg_attack_pos(y_current, start):
    sum = 0
    count = 0
    for i in range(start, len(y_current)):
        cell = str(y_current[i])
        if cell.find('^') >= 0 or cell.find('v') >= 0:
            cell = cell.replace('^', ' ')
            cell = cell.replace('v', ' -')
            try:
                num = int(cell[1:])
                sum += num
                count += 1

            except ValueError:
                pass
    if count == 0:
        return '#UND'
    return sum / count


