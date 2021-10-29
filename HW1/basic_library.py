# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 15:12:00 2021

@author: maxmi
"""

import random as rand

directions = ('N', 'E', 'S', 'W')

def generate_walk(blocks = 1):
    """
        Generates a list of directions
        blocks: the length of the list
    """
    walk = list()
    for x in range(blocks):
        walk.append(rand.choice(directions))
    
    return walk

def decode_walk(walk):
    """
        Decodes a walk and returns a tuple of int describing the position on a grid. Always starts at (0, 0)
        walk: a list of directions (see generate_walk function)
    """
    x = 0
    y = 0
    for d in walk:
        if (d == 'N'):
            y += 1
        elif (d == 'E'):
            x += 1
        elif (d == 'S'):
            y -= 1
        elif (d == 'W'):
            x -= 1
            
    return (x, y)

def distance_manhattan(start, end):
    """
        Calculates the manhattan distance between two points on a grid
        start: a tuple of integers e.g. (0, 0)
        end: a tuple of integers e.g. (2, 4)
    """
    return sum(abs(x - y) for x, y in zip(start, end))

def do_walk(blocks, dist = distance_manhattan):
    """
        Generates a walk and the distance of the final point to origin 
        blocks: how many steps the walk should include
        dist: the function used to calculate the distance, has to take 2 int tuples as param
    """
    walk = generate_walk(blocks)
    distance = dist((0, 0), decode_walk(walk))
    
    return (walk, distance)

def monte_carlo_walk_analysis(max_blocks, repetitions = 10000):
    """
        Generates repetitions amounts of walks for each stepsize from 1 to max_blocks and saves them in a dictionary
    """
    all_walks = dict()
    for length in range(1, max_blocks + 1):
        walks = list()
        for rep in range(repetitions):
            walks.append(do_walk(length))
        all_walks[length] = walks
        
    return all_walks