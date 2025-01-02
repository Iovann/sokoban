# Solveur Sokoban avec A*

Ce programme résout des puzzles Sokoban en utilisant l'algorithme A*. Il trouve le chemin optimal pour pousser toutes les boîtes vers leurs objectifs.

## Prérequis

- Python 3.x
- NumPy (`pip install numpy`)
- AIMA Python (bibliothèque d'Intelligence Artificielle)

## Installation

1. Clonez ce dépôt : git clone https://github.com/iovann/sokoban.git
2. Installez les dépendances : pip install numpy

3. Configurez le chemin AIMA dans `MySokoban.py` :
   - Remplacez `aima_path = "/home/iovann/Images/aima-python-master"` par le chemin réel de votre répertoire AIMA.


## Structure des fichiers

- `MySokoban.py` : Le solveur principal
- `sokobanLevels/` : Dossier contenant les niveaux au format .xsb
  - Format des niveaux :
    - `#` : Mur
    - `@` : Joueur
    - `$` : Boîte
    - `.` : Objectif
    - `X` : Boîte sur objectif
    - ` ` : Espace vide

## Utilisation

1. Placez votre fichier de niveau (.xsb) dans le dossier `sokobanLevels/`

2. Exécutez le solveur :

python MySokoban.py -l nom_du_niveau.xsb



## Comprendre la solution

La solution est une séquence de mouvements où :
- Lettres minuscules (u,d,l,r) : déplacement simple
- Lettres majuscules (U,D,L,R) : pousse une boîte
  - U/u : haut (up)
  - D/d : bas (down)
  - L/l : gauche (left)
  - R/r : droite (right)

## Sortie attendue

Le programme affichera :
1. Le niveau chargé
2. Les positions initiales
3. La solution trouvée par A*
4. La vérification de la solution
5. Le temps d'exécution

## Dépannage

Si vous rencontrez des erreurs :
1. Vérifiez que le chemin AIMA est correct
2. Assurez-vous que le fichier de niveau existe dans `sokobanLevels/`
3. Vérifiez que le format du niveau est valide

## Contribution

N'hésitez pas à contribuer en :
- Ajoutant de nouveaux niveaux
- Améliorant l'algorithme
- Signalant des bugs