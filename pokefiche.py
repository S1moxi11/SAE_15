import requests
from utils.download_cache import *
from utils.md_to_html import *
from utils.trad import *
import argparse
import webbrowser

parser = argparse.ArgumentParser()
parser.add_argument("poke", help="Entrez l'ID ou le nom d'un pokémon en anglais")
args = parser.parse_args()



def req(ch:str):
    return requests.get(ch).json()

def download_poke(id: int) -> dict:
   return req("https://pokeapi.co/api/v2/pokemon/"+str(id))

def poke_to_md(data: dict, filename: str) -> None:
    dico={}
    dico["height"]=data["height"]
    dico["weight"]=data["weight"]
    for stats in data["stats"]:
        if stats["stat"]["name"] == "hp":
            dico["hp"] = stats["base_stat"]
        elif stats["stat"]["name"] == "attack":
            dico["attack"] = stats["base_stat"]
        elif stats["stat"]["name"] == "defense":
            dico["defense"] = stats["base_stat"]
        elif stats["stat"]["name"] == "speed":
            dico["speed"] = stats["base_stat"]
    nb=1
    for i in data["types"]:
        dico["type "+str(nb)]=trad(i["type"]["url"])
        nb+=1
    types=""
    for key, value in dico.items():
        if key.startswith("type"):
            types += value.upper()+" "

    with open(filename, 'w') as f:
        f.write(f"# <center class='title'>HEY ! VOICI UNE FICHE SUR {str(trad(data['species']['url'])).upper()}</center>\n\n")
        f.write("## Informations principales\n")
        f.write(f"- **Poids :** {dico['weight']} kg\n")
        f.write(f"- **Taille :** {dico['height']} m\n")
        f.write(f"- **Type(s) :** {types.strip()}\n")
        f.write(f"- **Points de vie (HP) :** {dico['hp']}\n")
        f.write(f"- **Puissance d'attaque :** {dico['attack']}\n")
        f.write(f"- **Points de défense :** {dico['defense']}\n")
        f.write(f"- **Vitesse :** {dico['speed']}\n\n")
        if type(data["sprites"]["front_default"]) == str :
            f.write("![alt text]("+str(data["sprites"]["front_default"])+")")

            



def fiche_pokemon(id: int) -> None:
    poke_to_md(download_poke(id), "page_poke.md")
    convert("page_poke.md","page_poke.html")


with open("page_poke.css", 'w', encoding='utf-8') as f:
        f.write("""body {
    font-family: 'Arial', sans-serif;
    background-color: #f4f6f7;
    color: #2c3e50;
    margin: 0;
    padding: 0;
    text-align: center;
    line-height: 1.6;
}

.title {
    font-size: 4vw;
    color: #e74c3c;
    text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
    margin-bottom: 20px;
    padding-top: 20px;
    text-align: center;
}

h2 {
    font-size: 3vw;
    color: #34495e;
    border-bottom: 2px solid #3498db;
    padding-bottom: 5px;
    margin-bottom: 25px;
}

ul {
    list-style-type: none;
    padding-left: 0;
    margin-top: 20px;
    text-align: left;
    display: inline-block;
    font-size: 1.5em;
    max-width: 80%;
}

ul li {
    color: #34495e;
    margin-bottom: 12px;
    padding-left: 10px;
    position: relative;
}

ul li::before {
    content: "•";
    color: #e74c3c;
    font-size: 1.5em;
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
}

strong {
    font-weight: bold;
    color: #3498db;
}

img {
    max-width: 100%;
    height: auto;
    border-radius: 20px;
    border: 5px solid #3498db;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    margin-top: 30px;
    margin-bottom: 30px;
    transition: transform 0.3s ease-in-out;
}

img:hover {
    transform: scale(1.5);
}

footer {
    font-size: 1em;
    text-align: center;
    padding-top: 20px;
    padding-bottom: 20px;
    background-color: #ecf0f1;
    margin-top: 30px;
}

a {
    color: #3498db;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

@media (max-width: 600px) {
    .title {
        font-size: 6vw;
    }
    
    h2 {
        font-size: 4vw;
    }

    ul {
        font-size: 1.2em;
        max-width: 95%;
    }

    img {
        max-width: 90%;
    }
}

@media (min-width: 601px) and (max-width: 1024px) {
    .title {
        font-size: 4.5vw;
    }

    h2 {
        font-size: 3.5vw;
    }

    ul {
        font-size: 1.4em;
    }

    img {
        max-width: 80%;
    }
}

@media (min-width: 1025px) {
    .title {
        font-size: 2.8em;
    }

    h2 {
        font-size: 2.2em;
    }

    ul {
        font-size: 1.5em;
        max-width: 60%;
    }

    img {
        max-width: 400px;
    }
}
""")    


fiche_pokemon(args.poke)

webbrowser.open("page_poke.html")