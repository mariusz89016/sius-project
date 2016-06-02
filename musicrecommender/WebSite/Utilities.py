from DataLoader import GiveUsersForSite
from RBM import loadRBM
import numpy as np
import sqlite3
from mysite.models import Artists

class Utilities():
	def __init__(self,):
		self.rbm = loadRBM("/usr/src/app/WebSite/Best_RBM.npz")
		self.Users = GiveUsersForSite()


	def getArtistName(self, _id):
		return Artists.objects.get(id=_id).name

	def getArtistTags(self, _id):
		return Artists.objects.get(id=_id).tags

	def getUser(self, id):
		artists, grades = self.Users[int(id)]
		returnTup = []
		for i in range(len(artists)):
			returnTup += [(self.getArtistName(artists[i]), grades[i] , self.getArtistTags(artists[i]))]
		returnTup = sorted(returnTup, key=lambda x: -x[1])
		return returnTup

	def predictRBM(self, id, numberOfBest):
		prediction = self.rbm.prediction(self.Users[int(id)], isValidation = False)
		prediction = sorted(enumerate(prediction), key=lambda x:-x[1])[:numberOfBest]

		
		usersGrades = []
		for i in range(len(prediction)):
			usersGrades.append((self.getArtistName(prediction[i][0]), "{:.2f}".format(prediction[i][1]), self.getArtistTags(prediction[i][0])))

		return usersGrades

	def getUsersGrades(self, user_id):
		self.refresh()
		usersGrades = []
		self.cdb.execute("select artist_id, rank from ratings where user_id == '"+str(user_id)+"'")
		for f in self.cdb.fetchall():
			usersGrades.append((self.getArtistName(f[0]), str(f[1]), self.getArtistTags(f[0])))

		return usersGrades


	def getRandomUser(self):
		id = np.random.randint(0, len(self.Users))

		artists, grades = self.Users[id]

		returnTup = []

		for i in range(len(artists)):
			returnTup += [(self.getArtistName(artists[i]), grades[i], self.getArtistTags(artists[i]))]
		returnTup = sorted(returnTup, key=lambda x: -x[1])

		return returnTup, id
