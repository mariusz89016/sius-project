#in
inputFile = 'Data/artist_id_to_play_count.txt'
inputFile2 = 'Data/only_listened_artist_id_to_song_id.txt'
inputFile3 = 'Data/train_triplets.txt'

#out
outFile = 'Data/sparseData.txt'
outFile2 = 'Data/artistOrder.txt'

minPlayCount = 4

allPlayHistory = {}
sumPlayForUser = {}
song_id_to_artist_id = {}
artists = []
sortedArtists = []



def LoadArtistAndSort():
    global sortedArtists
    global artists


    with open(inputFile, encoding="utf-8") as fileWithArtistCount:
        for line in fileWithArtistCount:
            artist, playCount = line.replace("\n","").split(" ")
            if int(playCount) > minPlayCount:
               artists.append(artist)

    artists = sorted(artists)

    with open(outFile2, "w+", encoding="utf-8") as out:
        for i in range(0, len(artists)):
            out.write(artists[i]+"\n")
    print("Artist play count loaded")


def LoadSongToArtist():
    global song_id_to_artist_id
    with open(inputFile2) as songToArtist:
        for line in songToArtist:
            song, artist = line.replace("\n", "").split(" ")
            if artist in artists:
                song_id_to_artist_id[song] = artist
    print("Songs to Artist loaded")

def loadUserPlayHistory():
    global allPlayHistory
    global sumPlayForUser
    counter = 0
    with open(inputFile3) as data:
        for line in data:
            user, song, playCount = line.replace("\n", "").split("\t")

            if user in sumPlayForUser:
                sumPlayForUser[user] += int(playCount)
            else:
                sumPlayForUser[user] = int(playCount)

            if song in song_id_to_artist_id:
                if user in allPlayHistory:
                    allPlayHistory[user].append((song_id_to_artist_id[song], playCount))
                else:
                    allPlayHistory[user] = [(song_id_to_artist_id[song], playCount)]
            counter += 1
            if counter % 483735 == 0:
                print("parse " + str((counter/48373500.)*100.) + "%")

    print("Play History loaded")

def SavePlayHistoryAsMatrix():
    with open(outFile, "w+") as outH:
        counter = 0
        maxcounter = len(allPlayHistory.keys())
        for user in allPlayHistory.keys():
            tmpDict = {}
            playHistory = allPlayHistory[user]
            for artist, playCount in playHistory:
                if artist in tmpDict:
                    tmpDict[artist] += int(playCount)
                else:
                    tmpDict[artist] = int(playCount)

            orderTmpDict = sorted(tmpDict)

            outH.write(str(user)+"\t")
            outH.write(str(sumPlayForUser[user])+"\t")
            for artist in orderTmpDict:
                outH.write(artist+"\t"+str(tmpDict[artist])+"\t")

            outH.write("\n")
            if counter % 100 == 0:
                print(str(counter/float(maxcounter)*100.)+"%")
            counter += 1


LoadArtistAndSort()
LoadSongToArtist()
loadUserPlayHistory()
SavePlayHistoryAsMatrix()