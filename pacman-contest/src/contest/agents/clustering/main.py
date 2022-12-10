import argparse
from clustering_algorithm import AgglomerativeHierarchicalClustering
from matplotlib import pyplot as plt


def read_data(file_name, seperator=','):
    data = []
    with open(file_name) as input_file:
        for row in input_file.readlines():
            data.append([float(item) for item in row.split(seperator)])
    return data


ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True, help="path to input dataset")
ap.add_argument("-k", "--clusters", required=True, help="number of clusters")
ap.add_argument("-m", "--measure", required=True, help="distance measure. 0-single_link, 1-complete_link, 2-average_link")
args = vars(ap.parse_args())

dataset = read_data(args["dataset"], seperator=' ')
#print(type(dataset))
#print(type(dataset[0]))
print(dataset)

N = len(dataset)
K = int(args["clusters"])
M = int(args["measure"])

agg_hierarchical_clustering = AgglomerativeHierarchicalClustering(dataset, K, M)
agg_hierarchical_clustering.run_algorithm()
agg_hierarchical_clustering.print()

#plt.plot([var[0] for var in dataset], [var[1] for var in dataset], 'ro')
#plt.show()
print(len(agg_hierarchical_clustering.clusters.items()))
print(agg_hierarchical_clustering.clusters[0])

colors = ["b", "c", "g", "k", "m", "r", "y"]
markers = ["o", "s"]
for i in range(K):
    cluster = agg_hierarchical_clustering.clusters[i]
    plt.plot([var[0] for var in cluster], [var[1] for var in cluster], colors[i%len(colors)] + markers[i%len(markers)])
plt.xlim([0, max([var[0] for var in dataset])+2])
plt.ylim([0, max([var[1] for var in dataset])+2])
plt.show()

'''for id, points in self.clusters.items():
    print("Cluster: {}".format(id))
    for point in points:
        print("    {}".format(point))'''