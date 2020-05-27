import requests
from sheets import update_members, reset_trophies, update_wars
from funcs import get_time
import time


headers={
    'Accept':'application/json',
    'authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImYzMTMxNzZmLWUwODEtNDVmMi1iYTlhLWM1NDRkYzhmZmNkZiIsImlhdCI6MTU4OTc3NDY1NCwic3ViIjoiZGV2ZWxvcGVyLzI3YTNlOTk5LTI4OWItYTY5ZS1hODI4LTE0OTVjYjViZjM1YyIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjguMTkuNTYuMTc5Il0sInR5cGUiOiJjbGllbnQifV19.VIpI57HHPggv0-sWfPZsCadQuNAM0SOX1UiO2FaJBbwIirlGDKMNGAKMnBkTspuxG2DRQ3jRYsuYWNGUkMo3Qg'

}
CLAN_TAG = '%23P02CUUUU'

def get_user(tag):
    #return user's profile info
    response=requests.get('https://api.clashofclans.com/v1/players/%'+tag, headers=headers)
    user_json= response.json()
    print("_________________________________________")
    print("name= "+str(user_json['name']))
    print("Townhall LVL= " +str(user_json['townHallLevel']))
    print("Trophies= "+str(user_json['trophies']))
    print("_________________________________________")
    print("\n")


def show_clan():
    # return user's profile info
    response = requests.get('https://api.clashofclans.com/v1/clans/' + CLAN_TAG, headers=headers)
    clan_json = response.json()
    memberList=clan_json['memberList']
    for member in memberList:
        print("_________________________________________")
        print("name= ", member['name'])
        print("Tag= ",member['tag'])
        print("Level =", member['expLevel'])
        print("Current Trophies =", member['trophies'])
        print("TOTAL donations (in AND out)= ", str(member['donations']+member['donationsReceived']))
        print("_________________________________________")

def update_sheet():

    response = requests.get('https://api.clashofclans.com/v1/clans/' + CLAN_TAG, headers=headers)
    clan = response.json()

    reset_trophies()        # set all trophies to zero

    print(get_time() + ' - Trophies Reset.')

    clan = requests.get('https://api.clashofclans.com/v1/clans/' + CLAN_TAG, headers=headers).json()

    member_list = clan['memberList']
    update_members(member_list)

    print(get_time() + ' - Members Updated.')

    current_war = requests.get('https://api.clashofclans.com/v1/clans/' + CLAN_TAG + '/currentwar', headers=headers).json()
    update_wars(current_war)

    print(get_time() + ' - Wars Updated.')


update_sheet()

print(get_time() + ' - Program finish.')
