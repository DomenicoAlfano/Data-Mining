import hashlib
import numpy as np
import pickle
from collections import defaultdict
import itertools
from math import pow
import matplotlib.pyplot as plt
from algorithm import *
import time

def hashFamily(i):
  resultSize = 4        # how many bytes we want back
  maxLen = 20           # how long can our i be (in decimal)
  salt = str(i).zfill(maxLen)[-maxLen:]
  def hashMember(x):
    return int(hashlib.sha1((x + salt).encode()).hexdigest()[-resultSize:],16)
  return hashMember

#Here I implement LSH algorithm that, given a collection of minwise hash signatures of a set of documents, it finds the all the documents pairs that are near each other.
def LSH(collection_of_minwise_hash_signatures,bands,rows):
    start_time = time.time()
    threshold = pow((1/bands),1/rows)
    #Compressing hash matrix by bands and rows
    compressed_matrix = []

    column = []

    for element in collection_of_minwise_hash_signatures.T:
        for i in range(bands):
            block = element[i*rows:(i+1)*rows]
            el = ''
            for j in block:
                el+= str(int(j))
            column.append(el)
        compressed_matrix.append(column)
        column=[]

    #Hashing the new matrix
    
    new_matrix = np.array(compressed_matrix).T

    hashes = [hashFamily(i) for i in range(bands)]

    row = []

    new_hash_matrix = []

    for i in range(bands):
        for el in new_matrix[i]:
            row.append(hashes[i](str(el)))
        new_hash_matrix.append(row)
        row = []
    
    # Here I implement a list of dictionaries that takes as key the value of the hash and takes as value the documents with the same hash value

    list_of_dict = []

    for row in new_hash_matrix:
        d=defaultdict(list)
        for i,c in enumerate(row):
            d[c].append(i)
        list_of_dict.append(dict(d))

    # Then I create a dictionary that has as key the documents pairs that has the same hash value and as value the number of times that these pairs appears.

    #Finding duplicates pairs and near duplicates pairs for a given threshold 

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

    for k, v in new_dict.items():
        if v==bands:
            pairs_of_duplicates.append(k)
        if v!=bands and v/bands>threshold:
            pairs_of_near_duplicates.append(k)

    end=((time.time() - start_time))

    return pairs_of_duplicates, pairs_of_near_duplicates,end

def results():

    bands = [5,10,20]
    rows = [16,8,4]

    hash_matrix = pickle.load(open('../Problem_2_point_2/hash_matrix', 'rb'))
    
    lenght_LSH = []

    pond = []
    pod = []


    for i in range(len(bands)):
        pairs_of_duplicates, pairs_of_near_duplicates, end = LSH(hash_matrix,bands[i],rows[i])
        lenght_LSH.append(len(pairs_of_near_duplicates))
        pond.append(pairs_of_near_duplicates)
        pod.append(pairs_of_duplicates)

    print('Using LSH: The number of pairs of duplicates documents is: ' + str(len(pairs_of_duplicates))+' computed in '+str(end)+' seconds')

    print('The number of documents near duplicates founded by LSH with threshold = 80%'+' is: '+str(lenght_LSH[1])+' computed in '+str(end)+' seconds')

    # This line take so many time.
    # sets_of_objects = pickle.load(open('../Problem_2_point_2/10_shingling_all_documents', 'rb'))
    # pairs_of_duplicates_, pairs_of_near_duplicates_,end = algorithm_(sets_of_objects)

    pairs_of_duplicates_algorithm = pickle.load(open('pairs_of_duplicates_algorithm', 'rb'))

    pairs_of_near_duplicates_algorithm = pickle.load(open('pairs_of_near_duplicates_algorithm', 'rb'))

    end_ = pickle.load(open('end', 'rb'))

    print('Using the other algorithm: The number of pairs of duplicates documents is: ' + str(len(pairs_of_duplicates_algorithm))+' in '+str(end_)+' seconds')

    print('The number of documents near duplicates founded by the other algorithm with threshold = 80%'+' is: '+ str(len(pairs_of_near_duplicates_algorithm))+' in '+str(end_)+' seconds')

    print('The size of their intersection of duplicates is: '+str(len([list(filter(lambda x: x in pod[1], sublist)) for sublist in pairs_of_duplicates_algorithm])))

    fig, ax = plt.subplots(figsize=(8, 6))
    plt.bar(bands, lenght_LSH, align='center');
    plt.title('Number of documents near duplicates pairs found by LSH');
    plt.xlabel('Number of bands');
    plt.ylabel('Number of documents near duplicates pairs');
    plt.xticks(bands, bands);
    plt.show()


    return None

results()

