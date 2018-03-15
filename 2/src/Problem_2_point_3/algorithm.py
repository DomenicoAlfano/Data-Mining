import time
import numpy as np
import pickle
from collections import defaultdict
import itertools

def algorithm_(sets_of_objects):
    start_time = time.time()
    big_set = set()

    for shingles in sets_of_objects:
        for shingle in shingles:
            big_set.add(shingle)

    shingle_matrix=np.zeros((len(big_set),len(sets_of_objects)))

    list_of_dict = []

    for c,shingle in enumerate(big_set):
        d=defaultdict(list)
        for v,shingles in enumerate(sets_of_objects):
            if shingle in shingles:
                shingle_matrix[c][v] = 1
                d[shingle].append(v)
        list_of_dict.append(dict(d))

    new_dict = {}

    for el in list_of_dict:
        for values in el.values():
            for pair in itertools.combinations(values,2):
                if pair not in new_dict and pair[::-1] not in new_dict:
                    new_dict.setdefault(pair,0)
                if pair in new_dict:
                    new_dict[pair] += 1
                if pair[::-1] in new_dict:
                    new_dict[pair[::-1]] += 1

    pairs_of_duplicates = []
    pairs_of_near_duplicates = []

    t = 0.8

    for k, v in new_dict.items():
        if v==len(sets_of_objects[0]):
            pairs_of_duplicates.append(k)
        if v!=len(sets_of_objects[0]) and v/len(sets_of_objects[0])>=t:
            pairs_of_near_duplicates.append(k)

    end=((time.time() - start_time))

    pickle.dump(pairs_of_duplicates, open('pairs_of_duplicates_algorithm', 'wb'))

    pickle.dump(pairs_of_duplicates, open('pairs_of_near_duplicates_algorithm', 'wb'))

    pickle.dump(end, open('end', 'wb'))

    return pairs_of_duplicates, pairs_of_near_duplicates, end