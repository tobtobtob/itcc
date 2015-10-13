execfile('music_chains.py')

lengths = {
    '16':1,
    '8':2,
    '8.':3,
    '4':4,
    '4.':6,
    '2':8,
    '2.':12,
    '1':16}

def extract_pitch(note):
    return filter(lambda x: x not in map(str, range(10))+['.'], note)

def extract_time(note):
    return filter(lambda x: x in map(str, range(10))+['.'], note)

def create_rhythm(rhythm_chain, bars, last_time):
    while True:
        rhythm = rhythm_chain.generate(bars*16, last_time)
        rhythm_out = []
        counter = 0
        for r in rhythm:
            counter = counter + lengths[r]
            rhythm_out = rhythm_out + [r]
            if counter == bars*16:
                return rhythm_out

def create_melody(pitch_chain, rhythm_chain, bars, last_note):
    rhythm = create_rhythm(rhythm_chain, bars, extract_time(last_note))
    melody = pitch_chain.generate(len(rhythm), extract_pitch(last_note))
    return map(lambda a: a[0]+a[1], zip(melody, rhythm))

num_to_pitch = {52: "e",53: "f", 54: "fis",55: "g",56: "gis",57: "a",58: "ais",59: "b",60: "c'",
61: "cis'",62: "d'",63: "dis'",64: "e'",65: "f'",66: "fis'",
67: "g'",68: "gis'",69: "a'",70: "ais'",71: "b'",72: "c''",
73: "cis''",74: "d''",75: "dis''",76: "e''",77: "f''",78: "fis''",
79: "g''",80: "gis''",81: "a''",82: "ais''",83: "b''",84: "c'''",
85: "cis'''",86: "d'''"}

pitch_to_num = {"g":55,"gis":56,"a":57,"ais":58,"b":59,"c'":60,"cis'":61,"d'":62,
"dis'":63,"e'":64,"f'":65,"fis'":66,"g'":67,"gis'":68,"a'":69,"ais'":70,"b'":71,
"c''":72,"cis''":73,"d''":74,"dis''":75,"e''":76,"f''":77,"fis''":78,"g''":79,
"gis''":80,"a''":81,"ais''":82,"b''":83,"c'''":84,"cis'''":85,"d'''":86}

chords={'fis':-6, 'g':-5, 'gis':-4, 'a':-3, 'ais':-2, 'b':-1, 'c':0, 'cis':1, 'd':2,'dis':3,'e':4, 'f':5,
        'fis:m':4, 'g:m':5, 'gis:m':-6, 'a:m':-5, 'ais:m':-4, 'b:m':-3, 'c:m':-2, 'cis:m':-1, 'd:m':0,'dis:m':1,'e:m':2, 'f:m':3,
        'fis:7':-1, 'g:7':0, 'gis:7':1, 'a:7':2, 'ais:7':3, 'b:7':4, 'c:7':5, 'cis:7':-6, 'd:7':-5,'dis:7':-4,'e:7':-3, 'f:7':-2}

def transpose_to(what):
    def t(note):
        amount = chords[what]
        return num_to_pitch[pitch_to_num[note]+amount]
    return t

def transpose_from(what):
    def t(note):
        amount = chords[what]
        return num_to_pitch[pitch_to_num[note]-amount]
    return t

filename = "chorales.txt"

notes = open(filename, 'r').read().split()

only_pitch = map(extract_pitch, notes)
only_time = map(extract_time, notes)

pitch_chain = create(only_pitch, 3)
rhythm_chain = create(only_time, 3)

m = create_melody(pitch_chain, rhythm_chain, 4, "c'4")
print m

