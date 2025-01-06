# Choix pris

## Statistiques portées sur PC

- Nous avons choisi de porter principalement nos statistiques sur les points de combats des pokémons puisque nous avons trouvé cela original car il faut les calculer. Nous affichons ensuite les n pokémons ayant le plus de PC.

## Statistiques portées sur les Types

- Après avoir eu la liste des n pokémons ayant le plus de PC, on regarde les n types les plus retrouvés dans ces pokémons et on en fait un classement. Nous avons trouvé que cette idée était relativement intérressante car nous pouvons déterminer quels types ont le plus de pokemons avec le plus de pc.

# Difficultées rencontrées

- Certains pokémons ont plusieurs formes. Quand on traduit en francais ces pokemons, au lieu d'avoir un nom pour chaque forme, on a le même nom pour toutes. Quand je voulais afficher les n pokemons ayant le plus de pc et qu'il y avait un pokemon qui apparaissait sous plusieurs forme, ça me l'affichait qu'une seule fois.
Pour remédier a ce problème, si le nom du pokémon etait deja présent dans la liste des pokémons a afficher, j'ai ajouté un espace (" ") après le nom pour qu'il soit différent pour l'ordinateur mais pas pour nous.

- Lorsqu'on a créé le css pour pokestats, a cause de "md_to_html", le css s'appliquait sur pokefiche aussi. On a donc créé un css pour chacun et avec le nom de la page html et dans le code, on change juste l'extension pour qu'il prenne le fichier css.
Il a suffit de modifier une ligne du fichier css. Voici la ligne modifier : ```<link rel="stylesheet" href="{html_file[:-5]}.css">```

# Ce qu'on a appris

- Transformer un fichier md en html
- Créer un cache
- Créer / Utiliser des arguments avec argparse
- Utiliser le module get de la bibliothèque requests

# Avancement du projet

- Ce projet est fini mais m'a donné envie de refaire un projet a partir d'une base de données en ligne ou une API et d'en faire un jeu.
