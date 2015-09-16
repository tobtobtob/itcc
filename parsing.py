import json

def count_ys(y, filename):
    f = open(filename, 'r')
    dic = {}
    for line in f:
        if "as mysterious as" in line:
            temp = line.split()
            if dic.has_key(temp[4]):
                dic[temp[4]] = dic[temp[4]]+temp[6]
            else:
                dic[temp[4]] = temp[6]

    return dic

ddic = count_ys("mysterious", "n1000.txt")
print json.dump(ddic, indent=4)
