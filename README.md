# labyrinthGeneticSolver
## Solveur génétique de labyrinthe ASCII

Fonctionnement du code
I Modélisation du problème
Un labyrinthe de x*y cases est représenté par une matrice x*y où chaque case est une liste
de 4 bits disant si la direction est ouverte (0) ou fermée (1) dans l'ordre : bas, droite, haut, gauche
Ainsi, la suite 1100 représente une case de type _|, la suite 1001 : |_, etc...
On pourra représenter par la suite cette suite sous la forme d'un entier naturel de 0 à 15,
mais pour l'instant, par simplicité, on se contentera de le représenter sous forme binaire.
Précisons que le but du jeu sera ici de, partant de la case en haut à gauche (0,0), d'arriver à
la case en bas à droite (x,y).
EDIT : En réalité je me suis rapidement rendu compte qu'avec une représentation pareille du
labyrinthe, chaque barre était codée plusieurs fois, de plus le décodage du labyrinthe unicode généré
par le programme de Vidar Holen n'était pas décodé facilement en 'cases'. C'est pourquoi j'ai adopté
la représentation qui consiste à coder le labyrinthe en deux tableaux :
- mazeX code toutes les barres horizontales, de (0,0) en haut à gauche à (x,y) en bas à droite
- mazeY fait de même pour toutes les barres verticales.
Évidemment ce codage n'est pas très intuitif, c'est son défaut majeur, mais notons qu'en mêlant ces
deux tableaux on pourra facilement générer une matrice labyrinthe où les barres deviennent des
cases bloquées, et les cases vides seront à 0.


Exemple d'un labyrinthe unicode
II Génotype
Comme exposé dans le cours, on utilisera le codage de solution par position, qui apparemment
donne de meilleurs résultats que tout autre technique. Vu qu'il y a quatre directions possibles, on
représentera celle-ci par 2 bits dans l'ordre : 00 -> bas, 01 -> droite, 10 -> haut, et 11 -> gauche.
On représentera donc le génome d'une solution comme une matrice x*y (avec x et y taille du
labyrinthe) de 2 bits.III Objectif
La fonction objectif() fonctionnera simplement en testant la solution à partir de l'entrée du
labyrinthe,
en évaluant :
1) Se rapproche-t-on de la sortie ?
2) Si on arrive à la sortie, en combien de pas ?
On testera empiriquement les évaluations à attribuer à ces résultats.
IV Sélection des géniteurs
La sélection des géniteurs (fonction pick()) se fera par échantillonage stochastique (roulette de
casino),
parce que c'est la méthode explicitée dans le cours et que pour l'instant j'ai la flemme d'en apprendre
une autre.
On pourra en essayer d'autres plus tard, en gardant le programme assez modulaire pour supporter ce
type de changements.
V Croisements/Mutations
Le croisement se fera sur un ou deux cross-points (abscisse et ordonnés) choisis empiriquement.
On part d'une probabilité de 0.3 mutation par génération, mais on pourra lancer le dé plusieurs fois
pour que la solution puisse muter en différents points.
VI Interface
Le labyrinthe, que l'on peut générer à l'aide du programme generatemaze.py de Vidar Holen,
sera lu dans un fichier unicode dont le nom sera fourni en argument. Il sera alors décodé et gardé en
mémoire.
On créera d'abord la fonction stat() écrivant dans un fichier, pour chaque génération,
son score moyen, son meilleur élément, son pire élement, les géniteurs sélectionnés, etc...
Mais à terme j'aimerais créer une interface graphique dessinant les chemins des meilleurs/pires
solutions de chaque génération, ce qui est tout de même plus sympa.
Tests
Le code complet du programme se trouve dans le fichier Maze_gen/gen_lab.py
Testons le sur le labyrinthe 5*5 maze1 généré par le programme Maze_gen/generatemaze.py de
Vidar Holen, disponible sur la page http://www.vidarholen.net/~vidar/generatemaze.py :
Maze_gen$ ./gen_lab.py maze1

