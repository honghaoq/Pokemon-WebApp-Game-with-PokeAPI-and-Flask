from flask import Flask, url_for, render_template, redirect, jsonify, json, request
from requests import get
import urllib.request, urllib.error, urllib.parse, json, webbrowser, requests

# reference: https://github.com/pacman2020/Pokemon-flask-API

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


def get_poke_names(n=1000): # n is  limit 
    results = pokeAllREST(params={"limit": n})
    if results is None:
        return None
    else:
        all_poke = results.json()
        # print(pretty(all_poke))
        return all_poke


def get_poke_info(poke_id):
    result = pokeNameREST(id = poke_id)
    if result is None:
        return None
    else:
        this_poke = result.json()
        # print(pretty(this_poke))
        return this_poke

app = Flask(__name__)

@app.route('/')
def home():
    
    limit = 36
    offset  = request.args.get('offset')
    search = request.args.get('search')
    
    if search:
        pokemonsJson = get('https://pokeapi.co/api/v2/pokemon/'+search.lower())
        pokemon = json.loads(pokemonsJson.content)
        for i in pokemon['stats']:
            stat = i['base_stat']
            if i['stat']['name'] == "hp":
                hp = stat
            if i['stat']['name'] == "attack":
                attack = stat
            if i['stat']['name'] == "defense":
                defense = stat
            if i['stat']['name'] == "speed":
                speed = stat
        pokemons = []
        pokemons.append(
            {
                'id': pokemon['id'],
                'name': pokemon['name'],
                'type': pokemon['types'][0]['type']['name'],
                'experience': pokemon['base_experience'],
                'hp': hp,
                'attack': attack,
                'defense': defense,
                'speed': speed
            }
        )
        return render_template('home.html', pokemons=pokemons)
    
    url = 'https://pokeapi.co/api/v2/pokemon?limit={}&offset={}'.format(limit, offset)
    
    pokemonsJson = get(url)
    all_pokemons = json.loads(pokemonsJson.content)
    pokemons = []
    id = 0
    for pokemon in all_pokemons['results']:
        
        # extracting pokemon id by URL
        id_p = str(pokemon['url'])
        id = id_p.split('/')[-2]

        pokemon = get_poke_info(id)
        for i in pokemon['stats']:
            stat = i['base_stat']
            if i['stat']['name'] == "hp":
                hp = stat
            if i['stat']['name'] == "attack":
                attack = stat
            if i['stat']['name'] == "defense":
                defense = stat
            if i['stat']['name'] == "speed":
                speed = stat

        pokemons.append(
            {
                'id': id,
                'name': pokemon['name'],
                'type': pokemon['types'][0]['type']['name'],
                'experience': pokemon['base_experience'],
                'hp': hp,
                'attack': attack,
                'defense': defense,
                'speed': speed
            }
        )
    return render_template('home.html', pokemons=pokemons)

@app.route('/<name>')
def detail(name):
    pokemonsJson = get('https://pokeapi.co/api/v2/pokemon/'+name)
    pokemon_data = json.loads(pokemonsJson.content)
    for i in pokemon_data['stats']:
            stat = i['base_stat']
            if i['stat']['name'] == "hp":
                hp = stat
            if i['stat']['name'] == "attack":
                attack = stat
            if i['stat']['name'] == "defense":
                defense = stat
            if i['stat']['name'] == "speed":
                speed = stat
    pokemon ={
                'id': pokemon_data['id'],
                'name': pokemon_data['name'],
                'type': pokemon_data['types'][0]['type']['name'],
                'experience': pokemon_data['base_experience'],
                'hp': hp,
                'attack': attack,
                'defense': defense,
                'speed': speed
            }
    return render_template('detail.html', pokemon=pokemon)

if __name__ == '__main__':
    app.run(debug=True)