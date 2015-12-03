# -*- coding: utf-8 -*-
__author__ = 'Aleksadner'
import sqlite3

inputfile = 'Data/unique_tracks.txt'
outputfile = 'Data/artist_id_to_song_id.txt'
# Plik wynikiowy: 'id artysty' 'id piosenk'

dbFile = 'Data/track_metadata.db'

counter = 0

unique_songs_id = []

with open(inputfile,  encoding="utf8") as i:
    linesNo = len(i.readlines())

with open(inputfile,  encoding="utf8") as i:
    for iline in i:
        sline = iline.split("<SEP>")
        # print(iline)
        unique_songs_id += [sline[1]]
        counter += 1

        if counter % 1000 == 0:
            print("parsing" + str(counter) + "\\" + str(linesNo))


conn = sqlite3.connect(dbFile)
c = conn.cursor()

counter = 0
artist = c.execute("SELECT artist_id, song_id FROM songs")
artist_id_to_song_id = dict()
while True:
    tmpfetch = artist.fetchone()
    if tmpfetch == None:
        break
    artist_id_to_song_id[tmpfetch[1]] = tmpfetch[0]

linesNo = len(unique_songs_id)
	
with open(outputfile,  "w+", encoding="utf8") as o:
    for song_id in unique_songs_id:
        artist_id = artist_id_to_song_id[song_id]
        o.write(artist_id+" "+song_id+"\n")

        counter += 1
        if counter % 100 == 0:
            print("parse" + str(counter) + "\\" + str(linesNo))
#