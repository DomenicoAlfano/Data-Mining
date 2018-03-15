import hashlib
import pickle
import csv

def hashFamily(i):
  resultSize = 6        # how many bytes we want back
  maxLen = 20           # how long can our i be (in decimal)
  salt = str(i).zfill(maxLen)[-maxLen:]
  def hashMember(x):
    return int(hashlib.sha1((x + salt).encode()).hexdigest()[-resultSize:],16)
  return hashMember

#Here I implement how to choose a document (first long_description from Problem_1) and how I create its set of character shingles of some length k.
def shingling_and_hash(k):
    with open("../Problem_1/announcements.tsv") as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter="\t")
        k_shingling = []
        j = 0
        for line in tsvreader:
            if j < 1:
                j+=1
                list_of_char=[]
                for word in line[1]:
                    for char in word:
                        list_of_char.append(char)

                shingle = set ()

                for i in range(len(list_of_char)-k+1):
                    shingle.add(''.join(list_of_char[:k]))
                    list_of_char.pop(0)

                k_shingling.append(shingle)

    pickle.dump(k_shingling, open('k_shingling_one_document', 'wb'))

    #Then, I represent the document as the set of the hashes of the shingles, for 80 hash functions.

    number_hash_functions = 80

    hashes = [hashFamily(i) for i in range(number_hash_functions)]
    
    hash_set = set()
    
    hash_list = []
    
    hash_lists = []

    for i in range(number_hash_functions):
        for set_ in k_shingling:
            for shingle in set_:
                hash_set.add(hashes[i](shingle))
            hash_list.append(hash_set)
            hash_set=set()
        hash_lists.append(hash_list)
        hash_list = []

    pickle.dump(hash_lists, open('hash_lists', 'wb'))
    
    return hash_lists

hash_lists = shingling_and_hash(10)