import json

def count_ys(filename):
    f = open(filename, 'r')
    dic = {}
    counter = 0
    for line in f:
        if "as mysterious as" in line:
            temp = line.split()
            if dic.has_key(temp[4]):
                dic[temp[4]] = dic[temp[4]]+int(temp[6])
            else:
                dic[temp[4]] = int(temp[6])
                counter = counter+1

    return dic

ddic = count_ys("as_x.txt")

ddic_sorted = sorted(ddic, key=ddic.get, reverse=True)
print json.dumps(ddic, indent=4)
print json.dumps(ddic_sorted, indent=4)
