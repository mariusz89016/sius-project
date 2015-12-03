import numpy as np
import sqlite3

conn=sqlite3.connect('Data/database.sqlite3')
c = conn.cursor()

termConn = sqlite3.connect('../DataPreparation/Data/artist_term.db')
termC = termConn.cursor()

c.execute("CREATE TABLE \"mysite_artists\" (`id`	INTEGER, `name`	TEXT, `tags`	TEXT, PRIMARY KEY(id))")
conn.commit()

ArtistToID = np.load("../DataPreparation/Data/ArtistToID.npy").item()
ArtistToName = {}
mismatches_id = set()

with open('../DataPreparation/Data/sid_mismatches.txt', encoding="utf8") as i:
    for line in i:
        riline = line.replace("\n", "")
        mismatches_id.add(riline)

with open("../DataPreparation/Data/unique_artists.txt", encoding='utf-8') as artistFile:
    for line in artistFile:
        xline = line.replace("\n", "")
        sline = xline.split("<SEP>")

        if sline[2] not in mismatches_id:
            ArtistToName[sline[0]] = sline[3]

def getArtistTags(id):
    rstirng = ""
    termC.execute("select * from artist_term where artist_id == '"+id+"'")
    for tag in termC.fetchall():
        rstirng += tag[1] + ", "
    return rstirng[0:-2]

for artist in ArtistToID.keys():
    q = "INSERT INTO mysite_artists VALUES ('"+str(ArtistToID[artist])+"', '"+ArtistToName[artist].replace("'", "''")+"', '"+getArtistTags(artist).replace("'", "''")+"')"
    c.execute(q)
conn.commit()