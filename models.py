import datetime
import mysql.connector
from settings import CONFIG

class APIUserModel():
	def __init__(self):
		self.connection = mysql.connector.connect(**CONFIG)
		self.cursor = self.connection.cursor()

	def _close(self):
		self.connection.close()

	def get_by_id(self, id):
		try:
			sql = ("SELECT id, name, hash FROM api_users WHERE id = %s")
			self.cursor.execute(sql, (id, ))

			obj = False
			for (id, name, hash) in self.cursor:
				obj = {
					"id": id,
					"name": name,
					"hash": hash
				}

			return obj
		except Exception as e:
			raise False

	def get_by_name(self, name):
		try:
			sql = ("SELECT id, name, hash FROM api_users WHERE name = %s")
			self.cursor.execute(sql, (name, ))

			obj = False
			for (id, name, hash) in self.cursor:
				obj = {
					"id": id,
					"name": name,
					"hash": hash
				}

			return obj
		except Exception as e:
			return False

	def add(self, name, number=""):
		if self.get_by_name(name) == False:
			sql = ("INSERT INTO api_users (name, number) VALUES (%s, %s)")
			self.cursor.execute(sql, (name, number))
			self.connection.commit()

			sql = ("""CREATE TABLE IF NOT EXISTS api_%s_sents (
					number VARCHAR(100),
					message VARCHAR(5000),
					datetime VARCHAR(100)
				)
			""" % name)
			self.cursor.execute(sql)
			self.connection.commit()

	def register_sent(self, name, number,message):
		message = message.encode("utf-8")
		sql = ("INSERT INTO api_" + name + "_sents (number, message, datetime) VALUES (%s, %s, %s)")
		self.cursor.execute(sql, (number, message, datetime.datetime.now()))
		self.connection.commit()



