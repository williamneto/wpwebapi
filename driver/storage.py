"""
Modulo de gerenciamento de drivers

autor: William Neto <william.g.neto@gmail.com>
"""
import os
from webwhatsapi import WhatsAPIDriver

class DriversStorage():
	def __init__(self):
		self.drivers = []

	def new(self, user):
		profile = "profiles/%s/" % user
		media_location = "media/%s/" % user

		if not os.path.exists(profile):
			os.makedirs(profile)

		if not os.path.exists(media_location):
			os.makedirs(media_location)
 
		if self.get(user) == None:
			obj = {
				"user": user,
				"profile": profile,
				"media_location": media_location,
				"obj": WhatsAPIDriver(profile=profile, headless=True, loadstyles=True)
			}

			self.drivers.append(obj)
		else:
			obj_old = self.get(user)
			obj = self.get(user)
			obj["obj"] = WhatsAPIDriver(profile=profile, headless=True, loadstyles=True)

			self.drivers.remove(obj_old)
			self.drivers.append(obj)

		return obj

	def get(self, user):
		driver = None
		for d in self.drivers:
			if d["user"] == user:
				driver = d

		return driver