# credits: https://github.com/OlaPietka/Agglomerative-Hierarchical-Clustering-from-scratch

import math
#from measures import *

def distance(p, q):
    return math.sqrt(sum([(pi - qi)**2 for pi, qi in zip(p, q)]))


def single_link(ci, cj, dist):
    return min([dist(vi, vj) for vi in ci for vj in cj])


def complete_link(ci, cj, dist):
    return max([dist(vi, vj) for vi in ci for vj in cj])


def average_link(ci, cj, dist):
    distances = [dist(vi, vj) for vi in ci for vj in cj]
    return sum(distances) / len(distances)

def custom_link(ci, cj, dist):
    distances = [dist(vi, vj) for vi in ci for vj in cj]
    return sum(distances) / len(distances)


def get_distance_measure(M):
    if callable(M):
        return custom_link
    if M == 0:
        return single_link
    elif M == 1:
        return complete_link
    else:
        return average_link

class AgglomerativeHierarchicalClustering:
    def __init__(self, data, K, M):
        self.data = data
        self.N = len(data)
        self.K = K
        self.measure = get_distance_measure(M)
        self.distance = distance if not callable(M) else M
        self.clusters = self.init_clusters()

    def init_clusters(self):
        return {data_id: [data_point] for data_id, data_point in enumerate(self.data)}

    def find_closest_clusters(self):
        min_dist = math.inf
        closest_clusters = None

        clusters_ids = list(self.clusters.keys())

        for i, cluster_i in enumerate(clusters_ids[:-1]):
            for j, cluster_j in enumerate(clusters_ids[i+1:]):
                dist = self.measure(self.clusters[cluster_i], self.clusters[cluster_j], self.distance)
                if dist < min_dist:
                    min_dist, closest_clusters = dist, (cluster_i, cluster_j)
        return closest_clusters

    def merge_and_form_new_clusters(self, ci_id, cj_id):
        new_clusters = {0: self.clusters[ci_id] + self.clusters[cj_id]}

        for cluster_id in self.clusters.keys():
            if (cluster_id == ci_id) | (cluster_id == cj_id):
                continue
            new_clusters[len(new_clusters.keys())] = self.clusters[cluster_id]
        return new_clusters

    def run_algorithm(self):
        while len(self.clusters.keys()) > self.K:
            closest_clusters = self.find_closest_clusters()
            self.clusters = self.merge_and_form_new_clusters(*closest_clusters)

    def print(self):
        for id, points in self.clusters.items():
            print("Cluster: {}".format(id))
            for point in points:
                print("    {}".format(point))
    
    # type(data) == list
    def add_cluster(self, data):
        new_index = max(self.clusters.keys())+1
        self.clusters[new_index] =  data
        self.data.extend(data)
        return new_index

    def get_closest_cluster(self, id):
        min_dist = math.inf
        closest_cluster = None

        clusters_ids = list(self.clusters.keys())
        clusters_ids.remove(id)
        #print("IDs")
        #print(clusters_ids)

        for i, cluster_i in enumerate(clusters_ids[:-1]):
                dist = self.measure(self.clusters[cluster_i], self.clusters[id], self.distance)
                if dist < min_dist:
                    min_dist, closest_cluster = dist, cluster_i
        return self.clusters[closest_cluster]

    def get_cluster(self, id):
        return self.clusters[id]