mismatchesfile = 'Data/sid_mismatches.txt'
inputfile = 'Data/train_triplets.txt'
inputfile2 = 'Data/artist_id_to_song_id.txt'

outputfile = 'Data/only_listened_artist_id_to_song_id.txt'

songs_id = set()
mismatches_id = set()

with open(mismatchesfile, encoding="utf8") as i:
    for line in i:
        riline = line.replace("\n", "")
        mismatches_id.add(riline)

with open(inputfile, encoding="utf8") as i:
    for line in i:
        rline = line.replace("\n", "")
        sline = rline.split("\t")
        songs_id.add(sline[1])

onlyListenedSongs = songs_id - mismatches_id

song_id_to_artist_id = {}
with open(inputfile2,  encoding="utf8") as i:
    for line in i:
        rline = line.replace("\n", "")
        sline = rline.split(" ")
        song_id_to_artist_id[sline[1]] = sline[0]

with open(outputfile,  "w+", encoding="utf8") as o:
    for song in onlyListenedSongs:
        o.write(song+" "+song_id_to_artist_id[song]+"\n")