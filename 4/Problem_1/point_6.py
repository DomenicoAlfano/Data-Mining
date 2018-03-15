from pyspark import SparkContext, SparkConf
from itertools import combinations
from functools import partial

conf = SparkConf().setAppName('appName').setMaster('local')
sc = SparkContext(conf=conf)

name_file = 'facebook_combined.txt'

def compute_degree(name_file):

    file=open(name_file,'rb')

    dictionary = {}

    for line in file:
        nodes = [int(s) for s in line.split() if s.isdigit()]

        if nodes[0] not in dictionary:
            dictionary[nodes[0]] = 1
        else:
            dictionary[nodes[0]] += 1

        if nodes[1] not in dictionary:
            dictionary[nodes[1]] = 1
        else:
            dictionary[nodes[1]] += 1

        nodes = []

    return dictionary

def lowest_degree(edges,tuple_=False):
    if tuple_:
        u,v = edges[0],edges[1]
    else:
        u,v = edges.split()

    if dict_degree[int(u)] <= dict_degree[int(v)]:
        return (u,v)
    else:
        return (v,u)

def mr_WedgeEnumerator(edges, dict_degree):

    phase_1 = edges.map(lowest_degree)

    phase_2 = phase_1.groupByKey()

    phase_3 = phase_2.flatMapValues(partial(combinations,r=2))

    phase_4 = phase_3.map(lambda x: (x[0], (lowest_degree(x[1],True))))

    phase_5 = phase_4.map(lambda x: (x[1], x[0]))

    phase_6 = phase_1.map(lambda x: ((x),'$'))

    phase_7 = phase_5.union(phase_6)

    phase_8 = phase_7.groupByKey()

    phase_9 = phase_8.filter(lambda x: x if x[1] != '$' and '$' in x[1] else None)

    phase_10 = phase_9.map(lambda x: (x[0], [i for i in x[1] if i != '$'])).flatMapValues(lambda y: y).map(lambda x: (x[1], 1))

    phase_11 = phase_10.reduceByKey(lambda x, y: x + y)

    n_tr = sum(x[1] for x in phase_11.collect())

    return n_tr

def compute_clusteringCoeff(edges, top_10_nodes):
    phase_0 = edges.map(lowest_degree)
    # get all edges
    phase_1 = phase_0.union(phase_0.map(lambda x: (x[1], x[0])))
    # group keys
    phase_2 = phase_1.groupByKey()
    # get combinations
    phase_3 = phase_2.flatMapValues(partial(combinations, r=2))
    # invert key-value pairs
    phase_n = phase_3.map(lambda x: (x[0], (lowest_degree(x[1],True))))
    phase_4 = phase_n.map(lambda x: (x[1], x[0]))
    # join input and map output
    phase_nn = phase_0.map(lambda x: ((x),None))
    phase_5 = phase_4.union(phase_nn).map(lambda x: (x[0], '$') if not x[1] else x)
    # group keys
    phase_6 = phase_5.groupByKey()
    # filter edges
    phase_7 = phase_6.filter(lambda x: x if len(x[1]) > 1 or list(x[1])[0] != '$' else None)
    # get potential edges
    potential_edges = phase_7.map(lambda x: (x[0], [i for i in x[1] if i != '$'])).flatMapValues(
        lambda s: s).map(lambda x: (x[1], 1)).reduceByKey(lambda a, b: a + b)
    # get existing edges
    existing_edges = phase_7.filter(lambda x: x if '$' in x[1] else None).map(
        lambda x: (x[0], [i for i in x[1] if i != '$'])).flatMapValues(
        lambda s: s).map(lambda x: (x[1], 1)).reduceByKey(lambda a, b: a + b)
    # get clustering coefficients
    clustering_coefficients = dict(existing_edges.union(potential_edges).reduceByKey(
        lambda a, b: float(a) / b).collect())

    i=0
    for value in clustering_coefficients.values():
        i+=value

    average_clustering_coefficients=i/len(clustering_coefficients)

    cl_coeff_top_10 = {}

    for key in clustering_coefficients.keys():
        if int(key) in top_10_nodes:
            cl_coeff_top_10[key] = clustering_coefficients[key]

    return average_clustering_coefficients, cl_coeff_top_10

edges = sc.textFile(name_file)

dict_degree = compute_degree(name_file)

top_10_nodes = sorted(dict_degree, key=lambda x: dict_degree[x], reverse=True)[:10]

number_of_triangles = mr_WedgeEnumerator(edges, dict_degree)
print('The number of triangles is: '+str(number_of_triangles)+'\n')

average_clustering_coefficients, cl_coeff_top_10 = compute_clusteringCoeff(edges,top_10_nodes)
print('The average clustering coefficient is: '+str(average_clustering_coefficients)+'\n')

print('The clustering coefficient of the top 10 nodes by degree is:')
for key in cl_coeff_top_10.keys():
    print(str(key)+': '+str(cl_coeff_top_10[key]))
