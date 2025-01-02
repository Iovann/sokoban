import sys
import numpy as np
import time

# Configuration du chemin vers la bibliothèque AIMA pour l'algorithme A*
aima_path = "/home/iovann/Images/aima-python-master" 
# N'oubliez pas de remplacer le chemin par le chemin réel de votre répertoire AIMA
sys.path.append(aima_path)
from search import Problem, astar_search

class SokobanProblem(Problem):
    """Classe principale qui définit le problème Sokoban pour l'algorithme A*
    - initial: état initial (position joueur, position boîtes)
    - gameState: état complet du jeu
    """
    def __init__(self, initial, gameState):
        self.initial = initial
        self.gameState = gameState
        Problem.__init__(self, initial)
        
    def actions(self, state):
        """Retourne toutes les actions possibles pour un état donné"""
        return legalActions(state[0], state[1])
        
    def result(self, state, action):
        """Calcule le nouvel état après avoir effectué une action"""
        return updateState(state[0], state[1], action)
        
    def goal_test(self, state):
        """Vérifie si l'état actuel est l'état final (toutes les boîtes sur les objectifs)"""
        return isEndState(state[1])
        
    def h(self, node):
        """Fonction heuristique pour A* - estime la distance jusqu'à l'objectif"""
        return heuristic(node.state[0], node.state[1])

def transferToGameState(layout):
    """Convertit le layout textuel en matrice numérique
    0: espace vide
    1: mur
    2: joueur
    3: boîte
    4: objectif
    5: boîte sur objectif
    """
    layout = [x.replace('\n','') for x in layout]
    layout = [','.join(layout[i]) for i in range(len(layout))]
    layout = [x.split(',') for x in layout]
    maxColsNum = max([len(x) for x in layout])
    for irow in range(len(layout)):
        for icol in range(len(layout[irow])):
            if layout[irow][icol] == ' ': layout[irow][icol] = 0   
            elif layout[irow][icol] == '#': layout[irow][icol] = 1 
            elif layout[irow][icol] == '@': layout[irow][icol] = 2 
            elif layout[irow][icol] == '$': layout[irow][icol] = 3 
            elif layout[irow][icol] == '.': layout[irow][icol] = 4 
            elif layout[irow][icol] == 'X': layout[irow][icol] = 5 
        # Compléter les lignes plus courtes avec des murs
        colsNum = len(layout[irow])
        if colsNum < maxColsNum:
            layout[irow].extend([1 for _ in range(maxColsNum-colsNum)]) 
    return np.array(layout)

# Fonctions utilitaires pour obtenir les positions des éléments
def PosOfPlayer(gameState):
    """Retourne la position (x,y) du joueur"""
    return tuple(np.argwhere(gameState == 2)[0])

def PosOfBoxes(gameState):
    """Retourne les positions de toutes les boîtes (normales et sur objectif)"""
    return tuple(tuple(x) for x in np.argwhere((gameState == 3) | (gameState == 5)))

def PosOfWalls(gameState):
    """Retourne les positions de tous les murs"""
    return tuple(tuple(x) for x in np.argwhere(gameState == 1))

def PosOfGoals(gameState):
    """Retourne les positions de tous les objectifs"""
    return tuple(tuple(x) for x in np.argwhere((gameState == 4) | (gameState == 5)))

def isEndState(posBox):
    """Vérifie si toutes les boîtes sont sur les objectifs
    
    Args:
        posBox: tuple de tuples contenant les positions (x,y) des boîtes
        
    Returns:
        bool: True si toutes les boîtes sont sur des objectifs, False sinon
        
    Note:
        Utilise posGoals qui est une variable globale contenant les positions des objectifs
    """
    # Convertit les positions en ensembles pour une comparaison plus efficace
    box_positions = set(posBox)
    goal_positions = set(posGoals)
    
    # Vérifie si chaque boîte est sur un objectif
    return box_positions == goal_positions

def isLegalAction(action, posPlayer, posBox):
    """Vérifie si une action est légale:
    - Pas de collision avec un mur
    - Pas de collision avec une boîte immobile
    """
    xPlayer, yPlayer = posPlayer
    if action[-1].isupper(): # Action de pousser une boîte
        x1, y1 = xPlayer + 2 * action[0], yPlayer + 2 * action[1]
    else: # Simple déplacement
        x1, y1 = xPlayer + action[0], yPlayer + action[1]
    return (x1, y1) not in posBox + posWalls

def legalActions(posPlayer, posBox):
    """Génère toutes les actions légales possibles:
    - u/U: haut (minuscule=déplacement, majuscule=pousser)
    - d/D: bas
    - l/L: gauche
    - r/R: droite
    """
    allActions = [[-1,0,'u','U'],[1,0,'d','D'],[0,-1,'l','L'],[0,1,'r','R']]
    xPlayer, yPlayer = posPlayer
    legalActions = []
    for action in allActions:
        x1, y1 = xPlayer + action[0], yPlayer + action[1]
        if (x1, y1) in posBox: # Si une boîte est présente
            action.pop(2) # Garder l'action de pousser
        else:
            action.pop(3) # Garder l'action de déplacement
        if isLegalAction(action, posPlayer, posBox):
            legalActions.append(action)
    return tuple(tuple(x) for x in legalActions)

def updateState(posPlayer, posBox, action):
    """Met à jour l'état du jeu après une action:
    - Nouvelle position du joueur
    - Nouvelle position des boîtes si une boîte a été poussée
    """
    xPlayer, yPlayer = posPlayer
    newPosPlayer = [xPlayer + action[0], yPlayer + action[1]]
    posBox = [list(x) for x in posBox]
    if action[-1].isupper(): # Si on pousse une boîte
        posBox.remove(newPosPlayer)
        posBox.append([xPlayer + 2 * action[0], yPlayer + 2 * action[1]])
    posBox = tuple(tuple(x) for x in posBox)
    newPosPlayer = tuple(newPosPlayer)
    return newPosPlayer, posBox

def heuristic(posPlayer, posBox):
    """Calcule l'heuristique pour A*:
    Distance de Manhattan entre chaque boîte et l'objectif le plus proche
    """
    distance = 0
    completes = set(posGoals) & set(posBox)
    sortposBox = list(set(posBox).difference(completes))
    sortposGoals = list(set(posGoals).difference(completes))
    
    for i in range(len(sortposBox)):
        distance += (abs(sortposBox[i][0] - sortposGoals[i][0])) + (abs(sortposBox[i][1] - sortposGoals[i][1]))
    return distance

def aStarSearch():
    """Exécute l'algorithme A* pour trouver la solution"""
    print("\n=== Démarrage de A* Search ===")
    beginBox = PosOfBoxes(gameState)
    beginPlayer = PosOfPlayer(gameState)
    print(f"Position initiale du joueur: {beginPlayer}")
    print(f"Positions initiales des boîtes: {beginBox}")
    print(f"Positions des objectifs: {posGoals}")
    
    initial_state = (beginPlayer, beginBox)
    problem = SokobanProblem(initial_state, gameState)
    print("\nRecherche de solution en cours...")
    solution = astar_search(problem)
    
    if solution:
        actions = [action[-1] for action in solution.solution()]
        sequence = ''.join(actions)
        print(f"\nSolution trouvée!")
        print(f"Nombre de mouvements: {len(actions)}")
        print(f"Séquence de mouvements: {sequence}")
        return sequence
    else:
        print("\nAucune solution trouvée!")
        return None

def readCommand(argv):
    """Parse les arguments de la ligne de commande pour charger le niveau"""
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-l', '--level', dest='sokobanLevels',
                      help='level of game to play', default='test12.xsb')
    args = dict()
    options, _ = parser.parse_args(argv)
    with open('sokobanLevels/'+options.sokobanLevels,"r") as f: 
        layout = f.readlines()
    args['layout'] = layout
    return args

def testSequence(sequence):
    """Test une séquence de mouvements donnée"""
    print(f"\nTest de la séquence: {sequence}")
    beginBox = PosOfBoxes(gameState)
    beginPlayer = PosOfPlayer(gameState)
    
    current_pos = beginPlayer
    current_boxes = beginBox
    
    for move in sequence:
        # Convertir le mouvement en action
        if move.lower() == 'u':
            action = [-1,0,'u' if move.islower() else 'U']
        elif move.lower() == 'd':
            action = [1,0,'d' if move.islower() else 'D']
        elif move.lower() == 'l':
            action = [0,-1,'l' if move.islower() else 'L']
        elif move.lower() == 'r':
            action = [0,1,'r' if move.islower() else 'R']
            
        # Vérifier si le mouvement est légal
        if not isLegalAction(action, current_pos, current_boxes):
            print(f"Mouvement illégal: {move}")
            return False
            
        # Mettre à jour l'état
        current_pos, current_boxes = updateState(current_pos, current_boxes, action)
        
    # Vérifier si c'est une solution
    if isEndState(current_boxes):
        print("Séquence valide - Niveau résolu!")
        return True
    else:
        print("Séquence valide mais ne résout pas le niveau")
        return False

# Point d'entrée principal du programme
if __name__ == '__main__':
    time_start = time.time()
    print("=== Démarrage du jeu Sokoban ===")
    layout = readCommand(sys.argv[1:])['layout']
    print("\nChargement du niveau...")
    print("Layout du niveau:")
    for line in layout:
        print(line.strip())
        
    # Initialisation de l'état du jeu
    gameState = transferToGameState(layout)
    posWalls = PosOfWalls(gameState)
    posGoals = PosOfGoals(gameState)
    
    print("\nInitialisation terminée")
    print(f"Nombre de murs: {len(posWalls)}")
    print(f"Nombre d'objectifs: {len(posGoals)}")
    
    # Lancement de la recherche de solution avec A*
    sequence = aStarSearch()
    
    # Test de la séquence trouvée par A*
    if sequence:
        print("\n=== Test de la séquence trouvée par A* ===")
        testSequence(sequence)
    
    time_end=time.time()
    print('\nTemps d\'exécution total: %.2f secondes' %(time_end-time_start))