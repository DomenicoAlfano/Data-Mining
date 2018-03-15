import hashlib
import numpy as np
import pickle

def hashFamily(i):
  resultSize = 6        # how many bytes we want back
  maxLen = 20           # how long can our i be (in decimal)
  salt = str(i).zfill(maxLen)[-maxLen:]
  def hashMember(x):
    return int(hashlib.sha1((x + salt).encode()).hexdigest()[-resultSize:],16)
  return hashMember

#Here I implement a function, that given a collection of sets of objects (e.g., strings, or numbers), creates a minwise hashing based signature for each set.
def minwise_hashing(sets_of_objects):

    print('Creating big set..')
    big_set = set()

    for shingles in sets_of_objects:
        for shingle in shingles:
            big_set.add(shingle)

    print('Created')

    print('Creating shingle_matrix..')
    shingle_matrix=np.zeros((len(big_set),len(sets_of_objects)))

    for c,shingle in enumerate(big_set):
        for v,shingles in enumerate(sets_of_objects):
            if shingle in shingles:
                shingle_matrix[c][v] = 1


    print('Created')

    number_hash_functions = 80

    hashes = [hashFamily(i) for i in range(number_hash_functions)]

    shingles_hashed = []
    big_set_hashed = []

    print('Hashing the big set..')

    for i in range(number_hash_functions):
        for shingle in big_set:
            shingles_hashed.append(hashes[i](shingle))
        big_set_hashed.append(shingles_hashed)
        shingles_hashed = []

    print('Hashed')

    hash_matrix=np.zeros((number_hash_functions,len(sets_of_objects)))

    for i in range(number_hash_functions):
        for j in range(len(sets_of_objects)):
            hash_matrix[i][j] = 20000000000 #As infinite

    print('Computing hash matrix..')
    for k in range(number_hash_functions):
        for i in range(len(shingle_matrix)):
            for j,found in enumerate(shingle_matrix[i]):
                if found == 1.:
                    if big_set_hashed[k][i]<hash_matrix[k][j]:
                        hash_matrix[k][j]=big_set_hashed[k][i]

    print('Computed')

    pickle.dump(hash_matrix, open('hash_matrix', 'wb'))

    return hash_matrix

sets_of_objects = pickle.load(open('10_shingling_all_documents', 'rb'))
hash_matrix = minwise_hashing(sets_of_objects)
