# -*- coding: utf-8 -*-

"""
Simple Gentic Algorithm for evolving random strings to the desired 'text.'
author: mcor15
date: 25/02/20
"""
import random, sys, time, argparse
from operator import itemgetter


#<<<Command Line Args Parser>>>>
parser = argparse.ArgumentParser()
parser.add_argument("text", help="the string you want to evolve", type=str)
parser.add_argument("pop_size", help="size of population of solutions", type=int)
parser.add_argument("-gen_size", help="the number of generations to run, default: 50", type=int)
args = parser.parse_args()

#<<<<Global Vars>>>> OwO
answer = list(map(lambda char : ord(char), list(args.text))) #encode input string to 'ascii' codes
propulation_size = int(args.pop_size)
if not args.gen_size == None:
    generations = args.gen_size
else:
    generations = 50

def generate_random_solution():
    """generate_random_solution() Generates a random solution of random characters from [ ,!,..A..Z..a..z...~]."""
    global answer
    #codes for chars [ ,!..A..Z..a..z..~]
    chars = list(range(32,127))
    
    solution = []
    while len(solution) < len(answer): #generate random solutions to length of the true answer
        solution.append(random.choice(chars))
    return solution

def generate_random_population(size):
    """generate_random_population(size) Returns a population of random solutions of size provided."""
    population = []
    while len(population) < size:
        population.append(generate_random_solution())
    return population

def codes_to_string(solution):
    """codes_to_string(solution) Returns a decoded string of a coded solution."""
    string = []
    for c in solution:
        string.append(chr(c))
    return "".join(string)


def fitness_function(solution, answer):
    """fitness_function(solution, answer) Returns a fitness score of a solution compaired to the desired answer. This score is the absolute 'ascii' distance between characters."""
    score =0
    for i in range(len(answer)):
        score += (abs(solution[i]-answer[i]))
    return score

def score(population):
    """score(population) Scores a population of solutions. Return a list of (score, solution) touples."""
    global answer
    scored_population =[]
    for solution in population:
        scored_population.append((fitness_function(solution, answer),solution))
    return scored_population

def breed(population):
    """breed(population) Returns a new population of crossbred solution and good unchanged solutions."""
    global answer
    new_population =[]
    while len(new_population) != len(population):
        #Tournament, huzzah!
        contender1 = random.choice(population)
        contender2 = random.choice(population)
        winner1 = min([contender1,contender2],key=itemgetter(0))[1]#select the solution with the best fitness

        contender1 = random.choice(population)
        contender2 = random.choice(population)
        winner2 = min([contender1,contender2],key=itemgetter(0))[1]#select the solution with best fitness

        #2-point Crossover breeding or add to new population.
        if random.random()*100 <= 80: #70~80% chance of crossover 
            crossover_point1 =0
            crossover_point2 =0
            while crossover_point1 == crossover_point2:#make sure we get 2 different corssover points
                crossover_point1 = random.randint(1,len(winner1)-1)
                crossover_point2 = random.randint(1,len(winner1)-1)

            #sort lowest crossover to highest crossover
            temp = min(crossover_point1,crossover_point2)
            crossover_point2 = max(crossover_point1,crossover_point2)
            crossover_point1 = temp
            children= []

            #Crossover
            children.append(winner1[0:crossover_point1] + winner2[crossover_point1:crossover_point2] + winner1[crossover_point2:])
            children.append(winner2[0:crossover_point1] + winner1[crossover_point1:crossover_point2] + winner2[crossover_point2:])
            for child in children:
                new_population.append(child)
        else:#No crossover add to new population
            new_population.append(winner1);new_population.append(winner2)
    return new_population



def mutate(solution):
    """mutate(solution) Returns a mutated solution by character shift by 1 place."""
    workingset=list(range(ord(" "),ord("~")+1))
    new_solution=[]
    for cell in solution:
        if random.random() < (1/20): #1 in 20 chance to mutate cell.
            
            #Mutation is a character shift up or down alphanumericly.
            change = random.choice([-1,1])#Randomly choose up or down shift.
            if (cell + change) > workingset[-1]:#If hit upper bound, shift down.
                cell += -(change)
            elif (cell + change) < workingset[0]:#If hit lower bound shift up.
                cell += -(change)
            else:
                cell += change
        new_solution.append(cell)
    return new_solution

def mutator(population):
    """mutator(population) applys a mutate function to each member of the population. Returns mutated population."""
    new_population =[]
    for solution in population:
        new_population.append(mutate(solution))
    return new_population 

#Run GA...
population = generate_random_population(propulation_size) #generate initial population of solutions
ga_iterations=0
not_found = True
while not_found and ga_iterations < generations:
    #check population for correct solution
    for solution in population:
        if solution == answer: #Generated correct solution. :O
            not_found = False
            break
    print("Best solution of Generation {1}: {0}".format(codes_to_string(min(score(population),key=itemgetter(0))[1]), ga_iterations))#best solution so far..
    population = mutator(breed(score(population)))#breed and mutate new population
    ga_iterations +=1

if not not_found:
    print("Complete solution ({0}) found using GA in {1} iterations.".format(codes_to_string(solution),ga_iterations))
else:
    print("Best solution ({0}) found using Simple GA in {1} iterations.".format(codes_to_string(solution),ga_iterations))

