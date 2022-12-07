# baselineTeam.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# baselineTeam.py
# ---------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import random
import util

from captureAgents import CaptureAgent
from game import Directions
from util import nearestPoint
import time


#################
# Team creation #
#################

def create_team(first_index, second_index, is_red,
                first='StarvingPaccy', second='LittleGhostie', num_training=0):
    """
    This function should return a list of two agents that will form the
    team, initialized using firstIndex and secondIndex as their agent
    index numbers.  isRed is True if the red team is being created, and
    will be False if the blue team is being created.

    As a potentially helpful development aid, this function can take
    additional string-valued keyword arguments ("first" and "second" are
    such arguments in the case of this function), which will come from
    the --redOpts and --blueOpts command-line arguments to capture.py.
    For the nightly contest, however, your team will be created without
    any extra arguments, so you should make sure that the default
    behavior is what you want for the nightly contest.
    """
    return [eval(first)(first_index), eval(second)(second_index)]


##########
# Agents #
##########

class DumbAgent(CaptureAgent):
    def __init__(self, index, time_for_computing=.1):
        super().__init__(index, time_for_computing)
        self.start = None

    def register_initial_state(self, game_state):
        self.start = game_state.get_agent_position(self.index)
        CaptureAgent.register_initial_state(self, game_state)
    
    def choose_action(self, game_state):
        print("------------------------------------------------")
        # Najprej pridobi seznam vseh legalnih potez
        actions = game_state.get_legal_actions(self.index)

        # Pridobi oceno za koristnost vsake poteze
        values = [self.evaluate(game_state, action) for action in actions]
        max_value = max(values)
        best_actions = [action for action, value in zip(actions, values) if value == max_value]
        #print(values)
        
        return random.choice(best_actions)
    
    def get_successor(self, game_state, action):
        successor = game_state.generate_successor(self.index, action)
        position = successor.get_agent_state(self.index).get_position()
        if position != nearestPoint(position):
            return successor.generate_successor(self.index, action)
        else:
            return successor

    def evaluate(self, game_state, action):
        features = self.get_features(game_state, action)
        weights = self.get_weights(game_state, action)

        if type(self) == LittleGhostie:
            #print(features)
            #print(weights)
            print(features * weights)

        # vrne vsoto produktov istoimenskih komponent
        return features * weights

class LittleGhostie(DumbAgent):
    def get_features(self, game_state, action):
        features = util.Counter()

        # postavi se na potencialno naslednjo pozicijo
        successor = self.get_successor(game_state, action)

        my_state = successor.get_agent_state(self.index)
        my_pos = my_state.get_position()

        # preveri ali napadas ali branis (upostevaj tudi druge dejavnike, ne samo pozicijo)
        features['on_defense'] = 1
        if my_state.is_pacman or my_state.scared_timer > 0:
            features['on_defense'] = 0
        
        # Pridobi razdaljo do nasprotnikov (ce jih vidis)
        enemies = [successor.get_agent_state(opponent) for opponent in self.get_opponents(successor)]
        invaders = [enemy for enemy in enemies if enemy.is_pacman and enemy.get_position() is not None]
        features['num_invaders'] = len(invaders)
        
        # Preveri, ali je zmanjkalo kaj hrane
        if self.get_previous_observation() is not None:
            past_food = self.get_food_you_are_defending(self.get_previous_observation()).as_list()
            current_food = self.get_food_you_are_defending(game_state).as_list()
            missing_food = [food for food in past_food if food not in current_food]
            
            if len(missing_food) > 0:
                missing_food_dist = [self.get_maze_distance(my_pos, food) for food in missing_food]
                features['missing_food_distance'] = min(missing_food_dist)
        
        # preveri, kako dalec imas do najblizjega napadalca
        if len(invaders) > 0:
            distances = [self.get_maze_distance(my_pos, invader.get_position()) for invader in invaders]
            features['invader_distance'] = min(distances)
        
        # Preveri, kje se ti najbolj splaca cakati, ce ni nobenega dogajanja TODO: uporabi Tomazeve funkcije in zgoraj ustvarjene vrednosti
        
        # Pojma nimam, kaj je to ...
        if action == Directions.STOP:
            features['stop'] = 1

        rev = Directions.REVERSE[game_state.get_agent_state(self.index).configuration.direction]
        if action == rev:
            features['reverse'] = 1
        
        # return
        return features

    def get_weights(self, game_state, action):
        return {'on_defense': 100, 'num_invaders': -1000, 'missing_food_distance': -500, 'invader_distance': -10, 'stop': -100, 'reverse': -2}
































class StarvingPaccy(DumbAgent):
    def get_features(self, game_state, action):
        features = util.Counter()
        successor = self.get_successor(game_state, action)
        food_list = self.get_food(successor).as_list()
        #print(food_list)
        features['successor_score'] = -len(food_list)  # self.getScore(successor)

        # compute distance to opponents ghosts (if they are close)
        enemies = [successor.get_agent_state(i) for i in self.get_opponents(successor)]
        ghosts = [a for a in enemies if not a.is_pacman and a.get_position() is not None]
        features['num_ghosts'] = len(ghosts)
        #for i in ghosts:
        #    print(i.get_position())
        ghost_distances = [self.get_maze_distance(successor.get_agent_state(self.index).get_position(), a.get_position()) for a in ghosts]
        #print(features['num_ghosts'], ghost_distances)

        # Compute distance to the nearest food
        if len(food_list) > 0:  # This should always be True,  but better safe than sorry
            my_pos = successor.get_agent_state(self.index).get_position()
            min_distance = min([self.get_maze_distance(my_pos, food) for food in food_list])
            features['distance_to_food'] = min_distance
        return features

    def get_weights(self, game_state, action):
        return {'successor_score': 100, 'distance_to_food': -1}

