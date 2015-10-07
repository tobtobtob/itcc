import music_chains

filename = "notes.txt"

notes = open(filename, 'r').read().split()
only_pitch = map(lambda y : filter(lambda x: x not in map(str, range(10)), y), notes)

last_time = str(4)
def time_or_last_time(string):
    ret = filter(lambda x: x in map(str, range(10)), string)
    global last_time
    if ret == "":
        return last_time
    last_time = ret
    return ret

only_time = map(time_or_last_time, notes)
pitch_chain = create(only_pitch, 3)
time_chain = create(only_time, 3)

smoothing = lambda x: x+2

smooth(pitch_chain.chain, smoothing)
smooth(time_chain.chain, smoothing)

melody_length = 64

result = pitch_chain.generate(melody_length, "c'")
time_result = time_chain.generate(melody_length, "4")

score_start = "\\version \"2.18.2\"\n\score {\n<<\n{ \key c \major\n"
score_end = "\n}     \n>>\n\midi { }\n\layout { }\n}"

result = map(lambda x: x[0]+x[1], zip(result, time_result))
print result

result = score_start + ' '.join(result) + score_end
f = open("generated_score.ly", 'w')
f.write(result)
f.close()
