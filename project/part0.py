##############
# Your turn! #
##############

import urllib.request, urllib.error, urllib.parse, json, webbrowser, requests

#

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

#

def safe_get(url):
    r = requests.get(url)
    if r.status_code == 200:
        return requests.get(url)
    else:
        print("Failed to fulfill the request." )
        print("Error code: ", r.status_code)

#### Main Assignment ##############

#

def pokeAllREST(baseurl = 'https://pokeapi.co/api/v2/pokemon',
    params={},
    printurl = False
    ):
    url = baseurl + "?" + urllib.parse.urlencode(params)
    if printurl:
        print(url)
    return safe_get(url)

def pokeNameREST(baseurl = 'https://pokeapi.co/api/v2/pokemon/',
    id = 1,
    printurl = False
    ):
    url = baseurl + str(id)
    if printurl:
        print(url)
    return safe_get(url)

######################
## Building Block 1 ##
######################
#

def get_poke_names(n=1000): # n is  limit 
    results = pokeAllREST(params={"limit": n})
    if results is None:
        return None
    else:
        all_poke = results.json()
        # print(pretty(all_poke))
        return all_poke

######################
## Building Block 2 ##
######################
#

def get_poke_info(poke_id):
    result = pokeNameREST(id = poke_id)
    if result is None:
        return None
    else:
        this_poke = result.json()
        # print(pretty(this_poke))
        return this_poke

######################
## Building Block 3 ##
#######################
#

class Pokemon():
#     """A class to represent a Pokemon from PokeAPI"""
## 

    def __init__(self, this_poke):
        self.id = this_poke['id']
        self.name = this_poke['name']
        if this_poke['sprites']['other']['official-artwork']['front_default'] is None:
            self.url = this_poke['sprites']['other']['home']['front_default']
        else:
            self.url = this_poke['sprites']['other']['official-artwork']['front_default']
        self.experience = this_poke['base_experience']
        for i in this_poke['stats']:
            stat = i['base_stat']
            if i['stat']['name'] == "hp":
                self.hp = stat
            if i['stat']['name'] == "attack":
                self.attack = stat
            if i['stat']['name'] == "defense":
                self.defense = stat
            if i['stat']['name'] == "speed":
                self.speed = stat


## (b) __str__()
# The __str__() method should return a string with the statistics (experience / hp / attack / defense / speed) of each Pokemon

#
    def __str__(self):
        return 'Name: %s\nID: %s\nExperience: %s\nStats: \nHp:%s\nAttack:%s\nDefense: %s\nSpeed: %s\nurl: %s' % (self.name, self.id, self.experience, self.hp, self.attack, self.defense, self.speed, self.url)

def topPoke(poke_objects, attr): # attr has to be one of the stats: experience / hp / attack / defense / speed
    attr = attr.lower()
    if attr not in ['experience', 'hp', 'attack', 'defense', 'speed']:
        print('this attribute is not supported as input')
        return None
    else:
        print("\nTop Pokemons by "+ attr)
        print("------------")
        if attr == 'experience':
            pokestat = [x.experience for x in poke_objects]
        if attr == 'hp':
            pokestat = [x.hp for x in poke_objects]
        if attr == 'attack':
            pokestat = [x.attack for x in poke_objects]
        if attr == 'defense':
            pokestat = [x.defense for x in poke_objects]
        if attr == 'speed':
            pokestat = [x.speed for x in poke_objects]
        lst = []
        for i in range(len(pokestat)):
            lst.append([pokestat[i],i])
        lst.sort(reverse = True)
        sort_index = []
        for pairs in lst:
            sort_index.append(pairs[1])
        for i in range(10):
            print(poke_objects[sort_index[i]])
        return sort_index

if __name__ == '__main__':
    # ### Testing
    # print(pretty(get_poke_names(100)))
    # print(pretty(get_poke_info(1)['stats']))
    
    # pd = get_poke_info(1)
    # po = Pokemon(pd)
    # print(po)

    # ##############
    # ### Part 1 ###
    # ##############
    poke_names = get_poke_names(1118)  # max Pokemon # = 1118
    names = []
    for x in poke_names['results']:
        names.append(x['name'])
    # print(names)
    poke_objects = []
    count = 0
    for poke in names:
        poke_objects.append(Pokemon(get_poke_info(poke)))
        count +=1
        if count%50 == 0:
            print('%d pokemons processed' %(count))
    # poke_objects = [Pokemon(get_poke_info(poke)) for poke in names]
    # print(poke_objects[0])
    # webbrowser.open(poke_objects[0].url)
    

    # ##############
    # ### Part 2 ###
    # ##############
    # # Output an HTML page with the top ten Pokemons for experience, hp,
    # attack, defense and speed statistics. 

    # # #
    with open("poke.html","w",encoding="utf-8") as f:
        f.write("<html><head><title>Pokemons</title></head>")
        f.write("<body><h1>Top Pokemons based on Statistics</h1>")

        f.write("<p><b>Top 10 by hp:</b><br>")
        f.write("<div id='banner' style='overflow: hidden; display: flex; justify-content:space-around;'>")
        sort_index = topPoke(poke_objects, 'hp')
        for i in range(10):
            urli = poke_objects[sort_index[i]].url
            namei = poke_objects[sort_index[i]].name
            # f.write("<img src = '{url}' width='150' height='150' alt='{name}'>".format(url = urli, name = namei))
            # f.write("<figcaption> %s | %s </figcaption>" %(namei, poke_objects[sort_index[i]].hp))
            # f.write('%s | %s' %(namei, poke_objects[sort_index[i]].hp))
            f.write("<div class='' style='max-width: 100%; max-height: 100%;'>")
            f.write("<img src = '{url}' width='120' height='120' alt='{name}'>".format(url = urli, name = namei))
            f.write("<figcaption> %s (%s) </figcaption>" %(namei, poke_objects[sort_index[i]].hp))
            f.write("</div>")
        
        f.write("</div>")
        f.write("</p>")
        
        f.write("<p><b>Top 10 by experience:</b><br>")
        f.write("<div id='banner' style='overflow: hidden; display: flex; justify-content:space-around;'>")
        sort_index = topPoke(poke_objects, 'experience')
        for i in range(10):  
            urli = poke_objects[sort_index[i]].url
            namei = poke_objects[sort_index[i]].name
            f.write("<div class='' style='max-width: 100%; max-height: 100%;'>")
            f.write("<img src = '{url}' width='120' height='120' alt='{name}'>".format(url = urli, name = namei))
            f.write("<figcaption> %s (%s) </figcaption>" %(namei, poke_objects[sort_index[i]].experience))
            f.write("</div>")
        f.write("</div>")
        f.write("</p>")

        f.write("<p><b>Top 10 by attack:</b><br>")
        f.write("<div id='banner' style='overflow: hidden; display: flex; justify-content:space-around;'>")
        sort_index = topPoke(poke_objects, 'attack')
        for i in range(10):  
            urli = poke_objects[sort_index[i]].url
            namei = poke_objects[sort_index[i]].name
            f.write("<div class='' style='max-width: 100%; max-height: 100%;'>")
            f.write("<img src = '{url}' width='120' height='120' alt='{name}'>".format(url = urli, name = namei))
            f.write("<figcaption> %s (%s) </figcaption>" %(namei, poke_objects[sort_index[i]].attack))
            f.write("</div>")
        f.write("</div>")
        f.write("</p>")

        f.write("<p><b>Top 10 by defense:</b><br>")
        f.write("<div id='banner' style='overflow: hidden; display: flex; justify-content:space-around;'>")
        sort_index = topPoke(poke_objects, 'defense')
        for i in range(10):  
            urli = poke_objects[sort_index[i]].url
            namei = poke_objects[sort_index[i]].name
            f.write("<div class='' style='max-width: 100%; max-height: 100%;'>")
            f.write("<img src = '{url}' width='120' height='120' alt='{name}'>".format(url = urli, name = namei))
            f.write("<figcaption> %s (%s) </figcaption>" %(namei, poke_objects[sort_index[i]].defense))
            f.write("</div>")
        f.write("</div>")
        f.write("</p>")
        
        f.write("<p><b>Top 10 by speed:</b><br>")
        f.write("<div id='banner' style='overflow: hidden; display: flex; justify-content:space-around;'>")
        sort_index = topPoke(poke_objects, 'speed')
        for i in range(10):  
            urli = poke_objects[sort_index[i]].url
            namei = poke_objects[sort_index[i]].name
            f.write("<div class='' style='max-width: 100%; max-height: 100%;'>")
            f.write("<img src = '{url}' width='120' height='120' alt='{name}'>".format(url = urli, name = namei))
            f.write("<figcaption> %s (%s) </figcaption>" %(namei, poke_objects[sort_index[i]].defense))
            f.write("</div>")
        f.write("</div>")
        f.write("</p>")
        f.write("</body>")

        f.write("</html>")
