from sexpdata import loads, dumps

pitches = {
    55: "g",
    56: "gis",
    57: "a",
    58: "ais",
    59: "b",
    60: "c'",
    61: "cis'",
    62: "d'",
    63: "dis'",
    64: "e'",
    65: "f'",
    66: "fis'",
    67: "g'",
    68: "gis'",
    69: "a'",
    70: "ais'",
    71: "b'",
    72: "c''",
    73: "cis''",
    74: "d''",
    75: "dis''",
    76: "e''",
    77: "f''",
    78: "fis''",
    79: "g''",
    80: "gis''",
    81: "a''",
    82: "ais''",
    83: "b''",
    84: "c'''",
    85: "cis'''",
    86: "d'''"}

times = ["_","16","8","8.","4","_","4.","_","2","_","_","_","2.","_","_","_","1"]


data = open("choralesmod.lisp", 'r').read().split('&')
notes = ""

for d in data:
    d = loads(d)

    #transpose the note to keysign 0 (=c) with the lowest possible pitch change
   
    for line in d[1:]:
        keysign = line[3][1]
        pitch = line[1][1]
        if abs((keysign*7)%12) <= 6:
            pitch = pitch - ((keysign*7)%12)
        else:
            pitch = pitch + ((keysign*5)%12)
    
        notes = notes + pitches[pitch] + times[line[2][1]]+' '

output = open("chorales.txt", 'w')
output.write(notes)
output.close()

