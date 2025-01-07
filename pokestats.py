import requests
import math
import heapq
from utils.download_cache import *
from utils.trad import *
from utils.md_to_html import *
import webbrowser
from collections import Counter
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("sur_cb", help="Sur les combien de pokémons ayant le plus de pcs voulez-vous savoir quels sont les types les plus rencontrés ?", type=int)
parser.add_argument("cb_types", help="Combien de types voulez-vous voir dans les types les plus rencontrés dans la liste des n pokemons ayant le plus de pcs ?", type=int)
args = parser.parse_args()


def req(ch:str):
    """fait une requête HTTP GET à l'URL donnée et renvoie la réponse en format JSON. Arg = URL à interroger."""
    return requests.get(ch).json()


def get_dataset()->list:
    """cherche dans le cache"""
    L=[]
    for i in download("https://pokeapi.co/api/v2/pokemon/?limit=1302")["results"]:
        L.append(download_poke_cached(i["name"]))
    return L

dataset=get_dataset()

def compute_statistics(dataset=dataset, level=100):
    """Cette fonction renvoie un dictionnaire avec 
    le nom du pokemon en clé ainsi ses pc en valeur pour tous les pokémons"""
    dico = {}
    
    for i in dataset:
        nom, sta, vhp, vat, vdef = "", 0, 0, 0, 0
        nom = i["name"]
        
        for stats in i["stats"]:
            if stats["stat"]["name"] == "hp":
                vhp = stats["base_stat"]
            elif stats["stat"]["name"] == "attack":
                vat = stats["base_stat"]
            elif stats["stat"]["name"] == "defense":
                vdef = stats["base_stat"]

        sta = (0.01 * math.sqrt(vhp * vat * vdef)) * level
        dico[nom] = round(sta)
    return dico

"""print(compute_statistics)"""
top_10 = heapq.nlargest(10, compute_statistics().items(), key=lambda x: x[1])
"""top_50 = heapq.nlargest(50, compute_statistics().items(), key=lambda x: x[1])"""
"""print(top_10)"""

def trad_list(L):
    """traduis le nom / le type"""
    nvL=[]
    for i in L:
        nvL.append(((trad(download_poke_cached(i[0])["species"]["url"]),i[0]),i[1]))
    return nvL
    
"""print(trad_list(top_10))"""


def types_pokemons(data):
    """Renvoie un dictionnaire des types du pokemon -> type n : type"""
    dico={}
    nvdico={}
    nb=1
    for type in data["types"]:
        dico["type "+str(nb)]=trad(type["type"]["url"])
        nb+=1
    types=""
    for key, value in dico.items():
        if key.startswith("type"):
            types += value.upper()+" "
    nvdico[trad(data["species"]["url"])]=dico
    return nvdico

"""print(types_pokemons(dataset))"""

def moyenne_types(L):
    """Cette fonction renvoie le nombre de fois ou on croise un type dans le dictionnaire des pokemons ayant le plus de pc"""
    type_counter = Counter()
    for el in L:
        types_dict = types_pokemons(download_poke_cached(str(el[0][1])))
        for types in types_dict.values():
            type_counter[types['type 1']] += 1
            if 'type 2' in types:
                type_counter[types['type 2']] += 1
    return dict(type_counter)
    

"""print(moyenne_types(trad_list(top_10)))"""
"""leplus_types=heapq.nlargest(3, moyenne_types(trad_list(top_10)).items(), key=lambda x: x[1])"""
"""leplus_types=heapq.nlargest(3, moyenne_types(trad_list(top_50)).items(), key=lambda x: x[1])"""
"""print(leplus_types)"""
# Ici on renvoie les trois types les plus rencontrés dans la liste des 50 pokemons ayant le plus de pcs

def top_cmb(sur_cb:int, cb_types:int, dico_avec_noms_et_pcs: dict[str, int]):
    dico={}
    """cette fonction renvoie les n types rencontrés dans les n pokemons ayant le plus de pc"""
    top_n = heapq.nlargest(sur_cb, dico_avec_noms_et_pcs.items(), key=lambda x: x[1])
    top_n_fr=trad_list(top_n)
    espace=" "
    for i in top_n_fr:
        if not i[0][0] in dico :
            dico[i[0][0]]=download_poke_cached(i[0][1])["sprites"]["front_default"]
        else : 
            dico[i[0][0]+espace]=download_poke_cached(i[0][1])["sprites"]["front_default"]
            espace+=" "
    return dico, heapq.nlargest(cb_types, moyenne_types(trad_list(top_n)).items(), key=lambda x: x[1])

"""print(top_cmb(5,2,compute_statistics(get_dataset())))"""

def dataset_to_md(sur_cb: int, cb_types: int, donnees: dict, filename: str) -> None:
    stats = compute_statistics(donnees)
    dico, L = top_cmb(sur_cb, cb_types, stats)
    with open(filename, 'w') as f:
        f.write("<h1>HEY ! VOICI LA LISTE DES "+ str(sur_cb)+" POKÉMONS AYANT LE PLUS DE POINTS DE COMBAT</h1>")
        f.write("<ul>")
        i=1
        for pokemon_name, image_url in dico.items():
            f.write(f"""
            <li class="pokemon">
                <img src="{image_url}" alt="{pokemon_name}">
                <div class="pokemon-details">
                    <h3>{pokemon_name}</h3>
                    <p>{i}e Pokémon</p>
                </div>
            </li>
            """)
            i+=1

        f.write("</ul>")

        f.write("<div class='types-section'>")
        f.write("<h2>VOICI MAINTENANT LA LISTE DES "+ str(cb_types)+" TYPES QUE L'ON RETROUVE LE PLUS DANS CES POKÉMONS</h2>")
        f.write("<ul>")

        for type_name, count in L:
            f.write(f"<li>{type_name} - {count} occurrence(s)</li>")

        f.write("</ul>")
        f.write("</div>")
   

def infos_locales(sur_cb:int, cb_types:int) -> None:
    donnees = get_dataset()
    dataset_to_md(sur_cb, cb_types, donnees, "page_stats.md")
    convert("page_stats.md","page_stats.html")


with open("page_stats.css", 'w', encoding='utf-8') as f:
        f.write("""body {
    font-family: 'Poppins', sans-serif;
    background: #18e4ff;
    color: #333;
    margin: 20px;
    padding: 0;
    line-height: 1.6;
}

h1, h2 {
    text-align: center;
    color: #ff6f61;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
}

ul {
    list-style: none;
    padding: 0;
}

.pokemon {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #ffffff;
    border: 2px solid #ff6f61;
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 15px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.pokemon img {
    max-width: 100px;
    height: auto;
    border-radius: 50%;
    border: 3px solid #ff6f61;
    background-color: #ffe3e0;
}

.pokemon-details {
    flex: 1;
    margin-left: 20px;
}

.pokemon-details h3 {
    margin: 0;
    color: #444;
}

.pokemon-details p {
    margin: 5px 0;
    font-size: 0.9rem;
    color: #666;
}

.types-section {
    margin-top: 30px;
    padding: 20px;
    background: #f8f1f1;
    border: 2px solid #d7ccc8;
    border-radius: 10px;
}

.types-section h2 {
    color: #ff6f61;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

.types-section ul {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    padding: 0;
}

.types-section li {
    background: #ff6f61;
    color: #fff;
    margin: 5px;
    padding: 10px 15px;
    border-radius: 5px;
    font-weight: bold;
    font-size: 0.9rem;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
}

footer {
    text-align: center;
    margin-top: 40px;
    font-size: 0.8rem;
    color: #888;
}
""")

# ATTENTION !!! Ne pas mettre un chiffre trop grand pour le nombre de pokémons au risque d'attendre bcp (ex : environ 7 min pour 1000,10 quand le cache est téléchargé)
infos_locales(args.sur_cb,args.cb_types)

webbrowser.open("page_stats.html")