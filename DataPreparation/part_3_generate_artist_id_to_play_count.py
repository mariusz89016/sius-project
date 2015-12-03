__author__ = 'Aleksadner'

import operator

inputfile = 'Data/only_listened_artist_id_to_song_id.txt'
inputfile2 = 'Data/train_triplets.txt'

outputfile = 'Data/artist_id_to_play_count.txt';

song_id_to_artist_id = {}
artist_songs_count = {}
counter = 0

with open(inputfile) as i:
    for line in i:
        rline = line.replace("\n", "")
        sline = rline.split(" ")

        song = sline[0]
        artist = sline[1]

        song_id_to_artist_id[song] = artist

        if artist not in artist_songs_count:
            artist_songs_count[artist] = 0

with open(inputfile2) as i:
    for line in i:
        rline = line.replace("\n", "")
        sline = rline.split("\t")

        if(sline[1] in song_id_to_artist_id):
            artist_songs_count[song_id_to_artist_id[sline[1]]] += int(sline[2])
        counter += 1
        if counter % 483735 == 0:
            print("parse " + str((counter/48373500.)*100.) + "%") # \\ 48373500")

artist_songs_count = sorted(artist_songs_count.items(), key=operator.itemgetter(1))

with open(outputfile,  "w+") as o:
    for (artist, count) in artist_songs_count:
        o.write(artist+" "+str(count)+"\n")