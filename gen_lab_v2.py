#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import random, randint
from pprint import pprint
from copy import deepcopy
import sys
p = print
pp = pprint

def h(s) : 
	p(s,':',eval(s))

mazeX = mazeY = []  
sizeX = 0
sizeY = 0
MUR = '1'
OUVERT = '0'
Scores = []
ScoresPonderes = []
ScoreTotal = 0
ScoreMoyen = 0
BestScore = 0
PopSize = 500		# Nombre de candidats de chaque générations
MaxGen = 101 		# Nombre de générations successives
CrossNumber = 2		# Nombre de croisements 
CrossPointsNumber = 1 	# Nombre de points de croisements
MutateFactor = 1	# Chances de muter
MutateTry = 0		# Tentatives de mutations 

def readMaze(file="maze1") :		# Lit et stocke le labyrinthe dans les variables globales 
	global mazeX ; global mazeY ; global MutateTry
	try : lignes = open(file, 'r').read().split(' \n')
	except FileNotFoundError :
		print("Error : File", file, "doesn't exist !\nExit") 
		exit()
	x = int(len(lignes[0])/2)		# Longueur du labyrinthe (en cases)
	y = int(len(lignes)-1)			# Hauteur du labyrinthe (idem)
	mazeX = [ ['0' for a in range(x)] for b in range(y)]
	mazeY = [ ['0' for a in range(x+1)] for b in range(y-1) ]
	# Stockage des barres horizontales
	for i,ligne in enumerate(lignes) : 
		for z,c in enumerate(ligne[1::2]) :
			if c == '─' : mazeX[i][z] = MUR
			elif c == ' ' : mazeX[i][z] = OUVERT
			else : p("What the char :", c, "does here ??") ; exit()
	# p("Maze X :"); pp(mazeX) # Affichage de test
	# Stockage des barres verticales :
	for i,ligne in enumerate(lignes[:-2]) : 
		for z,c in enumerate(ligne[::2]) :
			if c in ['┬', '│', '├', '┤', '┼','┌','┐', '╷'] : mazeY[i][z] = MUR
			else : mazeY[i][z] = '0'
	# p("Maze Y :"); pp(mazeY) # Affichage de test
	global sizeX ; global sizeY
	sizeX = len(mazeX[0]) ; sizeY = len(mazeX)-1
	MutateTry = int(sizeY * sizeX / 3)
	print(MutateTry); input()
	return (mazeX, mazeY)

def generateRandomSolution() :		# Génére une solution aléatoirement
	res = [ [randint(0,3) for x in range(sizeX)] for y in range(sizeY)]
	return res

def generateNrandSolutions(n) :		# Génére N solutions aléatoirement
	resTab = [generateRandomSolution() for x in range(n)]
	return resTab

def objectif(solution, affiche=0, fromStart=0, amendeMur = -1, amendeBoucle = -1, amendeSortie = -1,
			gainProx = 5, gainAvance = 6, factorShort = 5, gainArrivé = 40) : # Calcule le score d'une solution
	scoreSolution = 0
	posParcourus = []
	pos = [0,0]
	# if fromStart or random() > 0.3 : pos = [0,0]
	# else : pos = [randint(0,sizeX-5),randint(0,sizeY-5)]
	proximite = 0
	while not(pos in posParcourus) and pos != [sizeX-1, sizeY-1] : # Tant qu'on boucle pas et qu'on n'a pas fini le maze
		posParcourus.append(pos.copy())
		x = pos[0] ; y = pos[1]
		#p("x:",x,"\ny:",y,"\nsolution:");pp(solution)
		try : move = solution[x][y]
		except IndexError : p("x:",x,"\ny:",y,"\nsolution:");pp(solution);exit()
		if not(move in [0,1,2,3]) : print("Move Error !") ; exit()
		if move == 0 : # bas
			if affiche : print("Bas")
			if mazeX[x+1][y] == MUR : scoreSolution += amendeMur ; break 
			pos[0] += 1
			scoreSolution += gainProx
		if move == 1 : # droite
			if affiche : print("Droite")
			if mazeY[x][y+1] == MUR : scoreSolution += amendeMur ; break 
			pos[1] += 1
			scoreSolution += gainProx
		if move == 2 : # haut
			if affiche : print("Haut")
			if mazeX[x][y] == MUR : scoreSolution += amendeMur; break 
			pos[0] -= 1
		if move == 3 : # gauche
			if affiche :  print("Gauche")
			if mazeY[x][y] == MUR : scoreSolution += amendeMur; break 
			pos[1] -= 1
		scoreSolution += gainAvance
		x = pos[0] ; y = pos[1]
		if x < 0 or x > sizeX-1 or y < 0 or y > sizeY-1 : 
			scoreSolution += amendeSortie
			if affiche : print("Sortie...")
			break # Fin de l'évaluation de cette solution
	if pos in posParcourus : scoreSolution += amendeBoucle
	if pos == [sizeX-1, sizeY-1] : scoreSolution += gainArrivé * (x*y)/len(posParcourus) * factorShort
	return scoreSolution

def stats(solutions) : # Actualise les scores d'une population donnée
	global Scores ; global ScoresPonderes ; global ScoreTotal ; global ScoreMoyen ; global BestScore
	Scores = [] ; ScoresPonderes = [] ; ScoreTotal = 0 ; ScoreMoyen = BestScore = 0
	for s in solutions :
		fitness = objectif(s)
		Scores.append(fitness)
		ScoreTotal += fitness
		if fitness > BestScore : BestScore = fitness
	for s in solutions : ScoresPonderes.append(max(objectif(s)/ScoreTotal,0)) ; 
	ScoreMoyen = ScoreTotal/PopSize

def printStats() :	# Affiche les stats de la population courante
	t = ["ScoreMoyen", "BestScore"]
	for i in t :
		p(i, ":", eval(i),"\n")

def pick(solutions, n = 0, niceFactor=0.9)  : # Sélectionne la prochaine populations # !!! Vérifier que N sortent bien !
	if n == 0 : n = PopSize
	newPop = []
	for i in range(n) :
		acc = 0				# Remarque importante : l'accumulateur EST remis à 0
		limite = random()*niceFactor
		for i,s in enumerate(ScoresPonderes) :
			acc += s
			if acc >= limite : newPop.append(deepcopy(solutions[i])) ; break
	while len(newPop) < n :
		newPop += [solutions[randint(0,len(solutions)-1)]]
	return newPop

def crossSolutions(solutions) :
	genList = pick(solutions, CrossNumber*2) # Sélectionne au hasard parmi les N meilleurs solutions
	for gen in genList : 
		try : solutions.remove(gen)
		except ValueError : '?'
	while genList :
		parent1 = genList.pop()
		parent2 = genList.pop()
		solutions += cross(parent1, parent2, randint(0,sizeX), randint(0,sizeY))
	return solutions

def cross(sol1, sol2, X, Y) :
	sol1 = deepcopy(sol1)
	sol2 = deepcopy(sol2)
	tmp1 = deepcopy(sol1)
	tmp2 = deepcopy(sol2)
	for y in range(Y, sizeY) :
		sol1[y] = sol1[y][:X] + tmp2[y][X:]
		sol2[y] = sol2[y][:X] + tmp1[y][X:]
	return [sol1, sol2]

def mutateSolutions(solutions) :
	s=deepcopy(solutions)
	for sol in solutions :
		for t in range(MutateTry) :
			if random() < MutateFactor :
				sol[randint(0,sizeY-1)][randint(0,sizeX-1)] = randint(0,3)
	return solutions

def main() :
	if len(sys.argv) > 1 : mazeFile = sys.argv[1]
	else : mazeFile = "maze1"
	readMaze(mazeFile)
	#pp(mazeX) # tests
	#pp(mazeY)
	#input()
	print(open(mazeFile).read())
	solutions = generateNrandSolutions(PopSize)
	for i in range(MaxGen) :
		p("**** Génération", i, " ****")
		stats(solutions)
		printStats()
		transcript(solutions[Scores.index(BestScore)])
		p("Meilleur combinaison :") ; 
		objectif(solutions[Scores.index(BestScore)],1,1)
		p();p()
		solutions = pick(solutions)
		solutions = crossSolutions(solutions)
		solutions = mutateSolutions(solutions)

def transcript(s) :
	for l in s :
		for e in l :
			if e == 0 : print('↓', end=' ') #←↑→↓
			if e == 1 : print('→', end=' ')
			if e == 2 : print('↑', end=' ')
			if e == 3 : print('←', end=' ')
		p()

def mazesToMatrix(mazeX, mazeY) :
	'a'

main()

"""
readMaze()
sols = generateNrandSolutions(2)
stats(sols)
CrossNumber=1
CrossPointsNumber=1
sol2 = cross(sols[0], sols[1], 5,5)
p();p()
pp(sols[0]) ; p("\t\t|\n\t\tV") ; pp(sol2[0]) ; p() ; p()
pp(sols[1]) ; p("\t\t|\n\t\tV") ; pp(sol2[1])
"""
"""
readMaze()
print(open("maze1").read())

PopSize = 44
sols = generateNrandSolutions(PopSize)
stats(sols)
p("Pop 1 :")
printStats()

sols = pick(sols)
p("\n** Pop 2 ;")
stats(sols)
printStats()
print(sols[Scores.index(BestScore)])
print(objectif(sols[Scores.index(BestScore)],1))

a=deepcopy(sols)
sols = crossSolutions(sols)
p(a==sols)"""