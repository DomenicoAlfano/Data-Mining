import csv
import itertools

def get_top_ten():
    reader = open('output_point_1.tsv')
    dic = {}

    #Create dictionary with pairs
    print('Creating the dictionary..')
    file = csv.reader(reader, delimiter='\t')
    for line in file:
        for pair in itertools.combinations(line[1:],2):
            if pair not in dic and pair[::-1] not in dic:
                dic.setdefault(pair,0)
            if pair in dic:
                dic[pair] += 1
            if pair[::-1] in dic:
                dic[pair[::-1]] += 1

    #sort by value
    print('Sorting..')
    dict_list = sorted(dic, key=dic.get, reverse=True)
    top_ten_pairs = dict_list[:10]

    #print out
    print('Writing..')
    f = open('top_ten_pairs.txt','w')
    for i,pair in enumerate(top_ten_pairs):
        f.write(str(i+1)+'. '+str(pair)+'\n')

    f.close()
    print('Finish !')

    return None

get_top_ten()