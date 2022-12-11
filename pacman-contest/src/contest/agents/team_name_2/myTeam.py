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

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helper

# (skoraj) kot pri  StarvingPaccy - za omogočanje napada (ko nasprotnik poje kapsulo) LittleGhostie-ju
def attack_mode(agent, game_state, action):
    def get_features(self, game_state, action):
        features = util.Counter()
        agent = game_state.data.agent_states[self.index]
        numCarrying = agent.num_carrying
        successor = self.get_successor(game_state, action)
        my_state = successor.get_agent_state(self.index)
        my_current_state = game_state.get_agent_state(self.index)
        past_position = None
        current_position = game_state.get_agent_position(self.index)
        my_pos = my_state.get_position()
        is_trapped = helper.is_trap(self.graph, current_position, my_pos)
        if self.get_previous_observation() is not None:
            past_position = self.get_previous_observation().get_agent_position(self.index)
        enemies = [successor.get_agent_state(opponent) for opponent in self.get_opponents(successor)]
        pacmans = [enemy for enemy in enemies if enemy.is_pacman and enemy.get_position() is not None]
        ghosts = [enemy for enemy in enemies if not enemy.is_pacman and enemy.get_position() is not None]
        food_list = self.get_food(successor).as_list()
        food_list_current = self.get_food(game_state).as_list()
        food_left = len(food_list_current)
        food_list_distances = [self.get_maze_distance(my_pos, food) for food in food_list]
        food_path = min(food_list_distances)
        layout = game_state.data.layout
        my_bases = [layout.agentPositions[i][1] for i in self.get_team(successor)]
        enemy_bases = [layout.agentPositions[i][1] for i in self.get_opponents(successor)]
        home_base_position = (my_bases[0][0], 0) if my_bases[0][0] == my_bases[1][0] else (0, my_bases[0][1])
        enemy_base_position = (enemy_bases[0][0], 0) if enemy_bases[0][0] == enemy_bases[1][0] else (0, enemy_bases[0][1])
        time_left = game_state.data.timeleft
        if home_base_position[0] > 0:
            dir = 0 if (layout.width - home_base_position[0]) < layout.width/2 else -1
            distances = [self.get_maze_distance(my_pos, (dir + layout.width/2, i)) for i in range(1, layout.height - 1) if not layout.walls[int(dir + layout.width/2)][i]]
        else:
            dir = 0 if (layout.height - home_base_position[1]) < layout.height/2 else -1
            distances = [self.get_maze_distance((i, dir + layout.width/2), my_pos) for i in range(1, layout.height - 1) if not layout.walls[i][int(dir + layout.width/2)]]
        dist = min(distances)
        retreat = False if ((time_left / 4 - 20) > dist) else True
        if food_left <= 2 or retreat:
            features['going_home'] = dist
            if len(ghosts) > 0:
                ghosts_dist = [self.get_maze_distance(current_position, ghost.get_position()) for ghost in ghosts]
                ghosts_current_dist = [self.get_maze_distance(my_pos, ghost.get_position()) for ghost in ghosts]
                ghost_approaching = min(ghosts_dist) - min(ghosts_current_dist)
                features['going_home_ghost_danger'] = ghost_approaching
            return features
        features['food_path'] = food_path
        features['food_eat'] = abs(len(food_list) - len(food_list_current))
        if len(ghosts) > 0:
            features['going_home'] = dist
            if len(ghosts) > 0:
                ghosts_dist = [self.get_maze_distance(current_position, ghost.get_position()) for ghost in ghosts]
                if (min(ghosts_dist) <= 2):
                    features.pop('food_eat', None)
                ghosts_current_dist = [self.get_maze_distance(my_pos, ghost.get_position()) for ghost in ghosts]
                ghost_approaching = min(ghosts_dist) - min(ghosts_current_dist)
                features['going_home_ghost_danger'] = ghost_approaching
            if (is_trapped):
                features['going_home_ghost_danger'] += 3
                features['going_home'] += 1
        if action == Directions.STOP:
            features['stop_move'] = 1
        rev = Directions.REVERSE[game_state.get_agent_state(self.index).configuration.direction]
        if action == rev:
            features['reverse_move'] = 1
        return features
    f = get_features(agent, game_state, action)
    print("features: " + str(f))
    return f

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

        # za shranjevanje rezultatov
        if os.path.exists("test.txt"):
            os.remove("test.txt")

    def register_initial_state(self, game_state):
        # dodaj graf labirinata (za potrebe pasti) - potrebno dobiti samo enkrat
        layout = str(game_state).split("\n")
        #print(layout)
        self.graph = helper.generate_graph_from_layout(layout)
        #print(self.graph)

        self.start = game_state.get_agent_position(self.index)
        CaptureAgent.register_initial_state(self, game_state)
    
    def choose_action(self, game_state):
        print("------------------------------------------------")
        # Najprej pridobi seznam vseh legalnih potez
        actions = game_state.get_legal_actions(self.index)

        # Pridobi oceno za koristnost vsake poteze
        values = [self.evaluate(game_state, action) for action in actions]

        # Pridobi vse najboljse poteze
        max_value = max(values)
        best_actions = [action for action, value in zip(actions, values) if value == max_value]

        if type(self) == StarvingPaccy:
            print([(x, y) for x, y in zip(actions, values)])
            print("[" + str(max_value) + "]")

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

        print(type(self))
        print(action)
        print(features)
        print(features * weights)
        #print(weights)

        # za shranjevanje podatkov v datoteke
        #if (type(self) == LittleGhostie):
        if (True):
            f = open("test.txt",'a')
            out = ""
            if (action == Directions.STOP):
                out += str(game_state)
            out += "\n" + str(type(self)) + "\n" + str(action) + "\n" + str(features) + "\n" + str(features * weights) + "\n\n"
            print(out, file=f)
            f.close()

        return features * weights

class StarvingPaccy(DumbAgent):
    def get_features(self, game_state, action):
        #self.layout = str(game_state)
        features = util.Counter()

        # da ve koliko hrane nosi
        agent = game_state.data.agent_states[self.index] # usefull
        numCarrying = agent.num_carrying

        # postavi se na potencialno naslednjo pozicijo
        successor = self.get_successor(game_state, action)
        my_state = successor.get_agent_state(self.index)
        my_current_state = game_state.get_agent_state(self.index)
        #print(my_current_state)
        #print(my_state)

        # pridobi pozicije in preveri, ali se premika v past
        past_position = None
        current_position = game_state.get_agent_position(self.index)
        my_pos = my_state.get_position();    #print(my_pos)  #print(current_position)
        is_trapped = helper.is_trap(self.graph, current_position, my_pos)
        #if is_trapped:
        #    features['is_trapped'] = 1


        if self.get_previous_observation() is not None:
            past_position = self.get_previous_observation().get_agent_position(self.index)

        # pridobi informacije o nasprotniku
        enemies = [successor.get_agent_state(opponent) for opponent in self.get_opponents(successor)]
        pacmans = [enemy for enemy in enemies if enemy.is_pacman and enemy.get_position() is not None]
        ghosts = [enemy for enemy in enemies if not enemy.is_pacman and enemy.get_position() is not None]

        food_list = self.get_food(successor).as_list()
        food_list_current = self.get_food(game_state).as_list()
        food_left = len(food_list_current)
        food_list_distances = [self.get_maze_distance(my_pos, food) for food in food_list]
        food_path = min(food_list_distances)

        layout = game_state.data.layout
        my_bases = [layout.agentPositions[i][1] for i in self.get_team(successor)]
        enemy_bases = [layout.agentPositions[i][1] for i in self.get_opponents(successor)]

        # za poiskat pot domov: ugotovis, o kateri koordinati govoris (vzhod-zahod [layout.width] ali sever-jug[layout.height]), 
        # potem pa isces min distance med sabo in tokami po liniji ob srediscu (width oziroma height) - 1
    
        home_base_position = (my_bases[0][0], 0) if my_bases[0][0] == my_bases[1][0] else (0, my_bases[0][1])
        enemy_base_position = (enemy_bases[0][0], 0) if enemy_bases[0][0] == enemy_bases[1][0] else (0, enemy_bases[0][1])
        #print(enemy_base_position, layout.height, layout.width)

        
        # preveri, na kateri polovici si
        # PAZI: GLEJ GLEDE NA TO, KAJ SI TRENUTNO, NE PA KAJ BOS V NASLEDNJEM KORAKU
        # preveri, ce sploh se imas dovolj casa
        if my_state.is_pacman:

            if len(pacmans)> 0:
                pacmans_distances = [self.get_maze_distance(my_pos, pacman.get_position()) for pacman in pacmans]
                minimal_pacman_distance = min(pacmans_distances)
                # če zelo stran od tebe: ne zanima
                if (minimal_pacman_distance <= 10):
                    features['pacman_nearby_distance'] = minimal_pacman_distance

            time_left = game_state.data.timeleft
            if home_base_position[0] > 0:
                dir = 0 if (layout.width - home_base_position[0]) < layout.width/2 else -1
                distances = [self.get_maze_distance(my_pos, (dir + layout.width/2, i)) for i in range(1, layout.height - 1) if not layout.walls[int(dir + layout.width/2)][i]]
            else:
                dir = 0 if (layout.height - home_base_position[1]) < layout.height/2 else -1
                distances = [self.get_maze_distance((i, dir + layout.width/2), my_pos) for i in range(1, layout.height - 1) if not layout.walls[i][int(dir + layout.width/2)]]
            dist = min(distances)

            retreat = False if ((time_left / 4 - 20) > dist) else True


            # najprej preveri, ce je nujno domov
            if food_left <= 2 or retreat:
                #dist = self.get_maze_distance(self.start, my_pos)
                features['going_home'] = dist
                if len(ghosts) > 0:
                    ghosts_dist = [self.get_maze_distance(current_position, ghost.get_position()) for ghost in ghosts]
                    ghosts_current_dist = [self.get_maze_distance(my_pos, ghost.get_position()) for ghost in ghosts]
                    ghost_approaching = min(ghosts_dist) - min(ghosts_current_dist)
                    features['going_home_ghost_danger'] = ghost_approaching
                return features # preveri ce je smiselno

            # si na nasprotnikovi polovici
            features['food_path'] = food_path
            features['food_eat'] = abs(len(food_list) - len(food_list_current))
            
            if len(ghosts) > 0:
                #print("danger")
                #features['ghosts_nearby_distance'] = min([self.get_maze_distance(my_pos, ghost.get_position()) for ghost in ghosts]) # preveri, ali je to potrebno
                features['going_home'] = dist
                if len(ghosts) > 0:
                    #features['testing'] = 1
                    ghosts_dist = [self.get_maze_distance(current_position, ghost.get_position()) for ghost in ghosts]
                    
                    # če ghost preblizu: ne pobirat - pomembno!!
                    if (min(ghosts_dist) <= 2):
                        features.pop('food_eat', None)
                    ghosts_current_dist = [self.get_maze_distance(my_pos, ghost.get_position()) for ghost in ghosts]
                    ghost_approaching = min(ghosts_dist) - min(ghosts_current_dist)
                    features['going_home_ghost_danger'] = ghost_approaching
                
                # če v pasti in duhci blizu -> raje iz pasti, ostalo "pozabi"
                # če ni duhcev blizu: ni pomembno
                if (is_trapped):
                    features['going_home_ghost_danger'] += 3
                    features['going_home'] += 1
                '''# če prazno: nevarnost me ne zanima toliko
                if (numCarrying == 0):
                    features['going_home_ghost_danger'] -= 1
                    features['going_home'] -= 1
                    pass'''

            if 2.5*numCarrying > len(food_list_current):
                features['going_home'] = dist * 10

            
        elif my_state.scared_timer > 0 and not my_state.is_pacman:
            # izogibaj se pacmanov
            if len(pacmans) > 0:
                pacman_distances_future = [self.get_maze_distance(my_pos, pacman.get_position()) for pacman in pacmans]
                pacman_distances_current = [self.get_maze_distance(current_position, pacman.get_position()) for pacman in pacmans]

                if len(pacman_distances_future) > 0 and len(pacman_distances_current) > 0:
                    future_min = min(pacman_distances_future)
                    current_min = min(pacman_distances_current)
                    diff = future_min - current_min
                    #print("diff" + str(diff))
                    features['pacman_danger_close'] = diff

            #print("RUNNN")
        
        else:
            pacmanDanger = False if len(ghosts) == 0 else True
            
            # če v moji polovici: izogni se duhcu, mogoče najde drugo pot
            if not my_current_state.is_pacman and pacmanDanger > 0:
                ghosts_dist = [self.get_maze_distance(current_position, ghost.get_position()) for ghost in ghosts]
                ghosts_current_dist = [self.get_maze_distance(my_pos, ghost.get_position()) for ghost in ghosts]
                ghost_approaching = min(ghosts_dist) - min(ghosts_current_dist)
                features['going_home_ghost_danger'] = ghost_approaching
                
            # Edge case - ce si trenutno pacman in nosis hrano / je v blizini duhec, se umakni na svojo polovico
            if my_current_state.is_pacman and (numCarrying or pacmanDanger) > 0: 
                features["drop_food"] = 1
            
            # Pojdi na nasprotnikovo polovico, vmes pa isci, ce je kje kaksen pacman -> ce je, ga napadi
            pacmans_distances = [self.get_maze_distance(my_pos, pacman.get_position()) for pacman in pacmans]
            if len(pacmans_distances) > 0:
                minimal_pacman_distance = min(pacmans_distances)
                features['pacman_nearby_distance'] = minimal_pacman_distance
            
            features['food_path'] = food_path
        
        # ni dobro če stojiš na mestu
        if action == Directions.STOP:
            features['stop_move'] = 1

        # ni ravno dobro če se vračaš
        rev = Directions.REVERSE[game_state.get_agent_state(self.index).configuration.direction]
        if action == rev:
            features['reverse_move'] = 1
        
        return features
    
    def get_weights(self, game_state, action):
        weights = util.Counter()
        weights['food_path'] = -5                  # 0, 1, 2, 3, 4 ........... | vecje je, dlje je hrana (vecje = slabse)
        weights['food_eat'] = 100                  # 0, 1 .................... | ali poje hrano s to potezo
        #weights['full'] = int(200)                     # ni v uporabi??
        weights['ghosts_nearby_distance'] = 10     # 0, 1, 2, 3, 4 ........... | vecje je, dlje je duhec (vecje = boljse)
        weights['pacman_danger_close'] = 40        # naceloma 0 ali 1, maybe 2 | vecje je, boljse je
        weights['pacman_nearby_distance'] = -1000  # 0, 1, 2, 3, 4 ........... | vecje je, dlje je pacman (vecje = slabse)
        weights['stop_move'] = -200                # 0, 1 .................... | zavraca neaktivnost
        weights['reverse_move'] = -2               # 0, 1 .................... | zavraca vracanje nazaj
        weights['going_home'] = -5                 # 0, 1, 2, 3, 4 ........... | vecje je, dlje je dom (vecje = slabse)
        weights['going_home_ghost_danger'] = -70   # naceloma 0 ali 1, maybe 2 | vecje je, slabse je
        weights['drop_food'] = 10000
        #weights['is_trapped'] = -5                 # 0, 1 .................... | ali se premika v past
        #weights['testing'] = 100000
        return weights


# tale se naj tudi ves cas premika proti najvecji gostoti svoje hrane -> utezi naj bodo majhne
class LittleGhostie(DumbAgent):
    def get_features(self, game_state, action):
        features = util.Counter()

        # postavi se na potencialno naslednjo pozicijo
        successor = self.get_successor(game_state, action)
        my_state = successor.get_agent_state(self.index)

        # pridobi pozicije
        past_position = None
        current_position = game_state.get_agent_position(self.index)
        my_pos = my_state.get_position()

        if self.get_previous_observation() is not None:
            past_position = self.get_previous_observation().get_agent_position(self.index)

        # pridobi informacije o nasprotniku
        enemies = [successor.get_agent_state(opponent) for opponent in self.get_opponents(successor)]
        pacmans = [enemy for enemy in enemies if enemy.is_pacman and enemy.get_position() is not None]
        ghosts = [enemy for enemy in enemies if not enemy.is_pacman and enemy.get_position() is not None]
        layout = game_state.data.layout

        my_food = [food for food in self.get_food_you_are_defending(game_state).as_list()]

        if my_state.scared_timer > 10:
            food_list = self.get_food(successor).as_list()
            food_list_distances = [self.get_maze_distance(my_pos, food) for food in food_list]
            food_path = min(food_list_distances)
            #features['food_path'] = food_path

            if my_state.is_pacman:
                # trenutno ne najjboljša opcija
                print("attack...\n\n\n")
                return attack_mode(self, game_state, action)
            # izogibaj se pacmanov in pojdi cim hitreje na nasprotnikovo polovico
            else:
                features['food_path'] = food_path
                if len(pacmans) > 0:
                    pacman_distances_future = [self.get_maze_distance(my_pos, pacman.get_position()) for pacman in pacmans]
                    pacman_distances_current = [self.get_maze_distance(current_position, pacman.get_position()) for pacman in pacmans]

                    if len(pacman_distances_future) > 0 and len(pacman_distances_current) > 0:
                        future_min = min(pacman_distances_future)
                        current_min = min(pacman_distances_current)
                        if future_min > current_min:
                            features['scared_avoiding_pacman'] = 1                    
                    #return attack_mode(self, game_state, action)        
        else:

            # če pacman in konec nevarnosti: takoj v obrambo
            if my_state.is_pacman:
                is_trapped = helper.is_trap(self.graph, current_position, my_pos)
                my_bases = [layout.agentPositions[i][1] for i in self.get_team(successor)]
                home_base_position = (my_bases[0][0], 0) if my_bases[0][0] == my_bases[1][0] else (0, my_bases[0][1])
                if home_base_position[0] > 0:
                    dir = 0 if (layout.width - home_base_position[0]) < layout.width/2 else -1
                    distances = [self.get_maze_distance(my_pos, (dir + layout.width/2, i)) for i in range(1, layout.height - 1) if not layout.walls[int(dir + layout.width/2)][i]]
                else:
                    dir = 0 if (layout.height - home_base_position[1]) < layout.height/2 else -1
                    distances = [self.get_maze_distance((i, dir + layout.width/2), my_pos) for i in range(1, layout.height - 1) if not layout.walls[i][int(dir + layout.width/2)]]
                dist = min(distances)
                features['going_home'] = 100*dist
                if len(ghosts) > 0:
                    ghosts_dist = [self.get_maze_distance(current_position, ghost.get_position()) for ghost in ghosts]
                    ghosts_current_dist = [self.get_maze_distance(my_pos, ghost.get_position()) for ghost in ghosts]
                    ghost_approaching = min(ghosts_dist) - min(ghosts_current_dist)
                    features['going_home_ghost_danger'] = ghost_approaching
                    if (is_trapped):
                        features['going_home_ghost_danger'] += 3
                        features['going_home'] += 1
            else:
                # poglej, ce ti kdo kaj je, pomakni se nekam v sredino, poskusi z blagim napadom
                if self.get_previous_observation() is not None:
                    past_food = self.get_food_you_are_defending(self.get_previous_observation()).as_list()
                    current_food = self.get_food_you_are_defending(game_state).as_list()
                    missing_food = [food for food in past_food if food not in current_food]

                    if len(missing_food) > 0:
                        # nekdo nekaj je, poisci ga
                        missing_food_dist = [self.get_maze_distance(my_pos, food) for food in missing_food]
                        features['missing_food'] = min(missing_food_dist)
                
                # preveri, ce imas koga v blizini
                pacmans_distances = [self.get_maze_distance(my_pos, pacman.get_position()) for pacman in pacmans]
                if len(pacmans_distances) > 0:
                    minimal_pacman_distance = min(pacmans_distances)
                    features['minimal_pacman_distance'] = minimal_pacman_distance
                
                # Tu pride Tomazeva funkcija za iskanje hrane (TODO) (preveri, kaj se zgodi, ce das to izven if stavka)
                my_food_distance = [self.get_maze_distance(my_pos, food) for food in my_food]
                resting_place_distance = int(sum(my_food_distance)/len(my_food_distance))
                features['resting_place_distance'] = resting_place_distance # spremeni to glede na to ali te ta smer spravi blizje srediscu ali ne
     
        # ni dobro če stojiš na mestu
        if action == Directions.STOP:
            features['stop'] = 1

        # ni ravno dobro če se vračaš
        rev = Directions.REVERSE[game_state.get_agent_state(self.index).configuration.direction]
        if action == rev:
            features['reverse'] = 1
        
        # return
        return features

    def get_weights(self, game_state, action):
        weights = util.Counter()
        weights['missing_food_distance'] = -1        # 0, 1, 2, 3, 4 ... | vecje je, dlje se slabo dogaja (vecje = slabse) (ko je pacman)
        weights['scared_avoiding_pacman'] = 100      # 0, 1 ............ | 1 if scared in v blizini pacmana else 0
        weights['food_path'] = -10                   # 0, 1, 2, 3, 4 ... | vecje je, dlje je hrana (vecje = slabse)
        weights['missing_food'] = -100               # 0, 1, 2, 3, 4 ... | vecje je, dlje se slabo dogaja (vecje = slabse) (isto kot missing_food_distance, samo da je tokrat kot ghost)
        weights['minimal_pacman_distance'] = -1000   # 0, 1, 2, 3, 4 ... | vecje je, slabse je
        weights['resting_place_distance'] = -1       # 0, 1, 2, 3, 4 ... | vecje je, slabse je
        weights['stop'] = -100                       # 0, 1 ............ | zavraca neaktivnost
        weights['reverse'] = -2                      # 0, 1 ............ | zavraca vracanje nazaj

        # weights from attack
        weights['food_eat'] = 100                  # 0, 1 .................... | ali poje hrano s to potezo
        weights['ghosts_nearby_distance'] = 10     # 0, 1, 2, 3, 4 ........... | vecje je, dlje je duhec (vecje = boljse)
        weights['pacman_danger_close'] = 40        # naceloma 0 ali 1, maybe 2 | vecje je, boljse je
        weights['pacman_nearby_distance'] = -1000  # 0, 1, 2, 3, 4 ........... | vecje je, dlje je pacman (vecje = slabse)
        weights['stop_move'] = -100                # 0, 1 .................... | zavraca neaktivnost
        weights['reverse_move'] = -2               # 0, 1 .................... | zavraca vracanje nazaj
        weights['going_home'] = -5                 # 0, 1, 2, 3, 4 ........... | vecje je, dlje je dom (vecje = slabse)
        weights['going_home_ghost_danger'] = -70   # naceloma 0 ali 1, maybe 2 | vecje je, slabse je
        weights['drop_food'] = 10000
        return weights