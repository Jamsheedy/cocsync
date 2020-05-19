import requests


headers={
    'Accept':'application/json',
    'authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImQ3YTRiZTJlLTBhMzAtNDJhNC1hZjMwLTlmZTMyODgxMTZiYiIsImlhdCI6MTU4OTkwNDQ2NSwic3ViIjoiZGV2ZWxvcGVyL2MxNzVjMmE1LWZmNzMtOGExZS1mOWUyLWM1YjdhMDg4NThiOCIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjk2LjU4LjE2Ny4xNTkiXSwidHlwZSI6ImNsaWVudCJ9XX0.VkrUEIejazU0v5mbA-8kO44bv5b0U79NQVU7piFj0Od7wXOBn2pOmHE_tXidHWCc_fAusf-F4G5zhrUxT81QoQ'



}

def get_user(tag):
    #return user's profile info
    response=requests.get('https://api.clashofclans.com/v1/players/%23'+tag, headers=headers)
    user_json= response.json()
    print("_________________________________________")
    print("name= ",str(user_json['name']))
    print("Townhall LVL= " ,str(user_json['townHallLevel']))
    print("Trophies= ",str(user_json['trophies']))
    print(user_json['tag'])
    print("_________________________________________")
    print("\n")


def show_clan():
    # return user's profile info
    response = requests.get('https://api.clashofclans.com/v1/clans/%23P02CUUUU', headers=headers)
    clan_json = response.json()
    #print(clan_json)
    print("name = ", str(clan_json['name']))
    print(clan_json['memberList'])
    memberList=clan_json['memberList']
    for member in memberList:
        print("_________________________________________")
        print("name = ", member['name'])
        rolestr=member['role']
        rolestr=rolestr.replace('admin', 'Elder')
        print("Role in clan = clan",rolestr )
        tagstr=str(member['tag'])
        tagstr=tagstr.replace("#","")
        print("Player tag = ", tagstr)
        print("Level =", member['expLevel'])
        print("Current Trophies =", member['trophies'])
        print("TOTAL donations (in AND out)= ", str(member['donations']+member['donationsReceived']))
        print("_________________________________________")

show_clan()
answer=input("Do you want to search for a individual user? Y/N: ")
while answer != 'Y' and answer !='N':
    print("Invalid option try again")
    answer = input("Do you want to search for a individual user? Y/N: ")
while answer == 'Y':
    tag = input("Enter the user's tag you want to search for: ")
    get_user(tag)
    answer = input("Do you want to search for a individual user? Y/N: ")
