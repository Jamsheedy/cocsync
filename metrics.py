from funcs import get_time


def update_metrics(sheet):
    header = sheet.getRow(2)
    try:
        average_stars_col = header.index('AVG Stars') + 1
        war_efficiency_col = header.index('War Efficiency') + 1
        start_war = header.index('Attack 1')
    except ValueError:
        print(get_time() + ' - ERROR: {AVG Stars} not in sheet row 2!')
        return

    avg_list = sheet.getColumn(average_stars_col)               # columns that are being updated
    wef_list = sheet.getColumn(war_efficiency_col)

    for i in range(2, len(avg_list)):
        player_row = sheet.getRow(i + 1)        # get player row from column

        # ATTRIBUTES WE ARE STORING
        # note: we only use one api request for n attributes
        avg_list[i] = get_avg_stars(player_row, start_war)
        wef_list[i] = get_war_efficiency(player_row, start_war)
    # end for loop

    # update attribute lists to their respective columns
    sheet.updateColumn(average_stars_col, avg_list)
    sheet.updateColumn(war_efficiency_col, wef_list)

    # all metrics up to date
    print(get_time() + ' - Metrics Updated')


# function definitions for the function definitions for every metric

def get_avg_stars(y_current, start):
    star_list = []
    for i in range(start, len(y_current)):
        try:
            star = int(y_current[i])  # get the cell in player row
            if 3 >= star >= 0:
                star_list.append(star)
            # else is not a star, could be clan games, maybe decimals im not sure
        except ValueError:  # its a string, or dash, so we do nothing
            pass

    # selective output
    if len(star_list) == 0:
        return -1
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
        return -1

    return round(attacks_used / attacks_available * 100, 2)
