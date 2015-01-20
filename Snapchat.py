import sys
import hashlib
import json
import requests
import time
import base64
from Crypto.Cipher import AES

class Snapchat:
	URL_BASE = "https://feelinsonice.appspot.com"
	STATIC_TOKEN = "m198sOkJEn37DjqZ32lpRu76xmw288xSQ9"
	ENCRYPT_KEY_2 = "M02cnQ51Ji97vwT4"
	REQ_TOKEN_PATTERN = "0001110111101110001111010101111011010001001110011000110001000110"
	REQ_TOKEN_SECRET = "iEk21fuwZApXlz93750dmW22pw389dPwOk"
	USERNAME = ""
	AUTH_TOKEN = ""
	unpad = lambda self, s : s[0:-ord(s[-1])]

	def request_token(self, auth_token, timestamp):
	    first = hashlib.sha256(self.REQ_TOKEN_SECRET + auth_token).hexdigest()
	    second = hashlib.sha256(str(timestamp) + self.REQ_TOKEN_SECRET).hexdigest()
	    bits = [first[i] if c == "0" else second[i] for i, c in enumerate(self.REQ_TOKEN_PATTERN)]
	    return "".join(bits)

	def get_time(self):
		return str(time.time())[:10]

	def login(self, username, password):
		self.USERNAME = username
		time = self.get_time()
		req_token = self.request_token(self.STATIC_TOKEN, time)
		r = requests.post(self.URL_BASE + "/bq/login", data={
	    "req_token": req_token,
	    "timestamp": time,
	    "username": username,
	    "password": password
		}, headers={"User-agent": None})
		auth_token, username = r.json()["auth_token"], r.json()["username"]
		self.AUTH_TOKEN = auth_token
		return 1 if len(self.AUTH_TOKEN) != 0 else 0

	def get_snap_list(self):
		time = self.get_time()
		req_token = self.request_token(self.AUTH_TOKEN, time)
		r = requests.post(self.URL_BASE + "/bq/updates", data={
	    "req_token": req_token,
	    "timestamp": time,
	    "username": self.USERNAME,
		}, headers={"User-agent": None})
		unread_snaps = []
		for jsonObject in r.json()["snaps"]:
			if(jsonObject["st"] == 1):
				unread_snaps.append(jsonObject)
		return unread_snaps

	def decrypt(self, data):
		if len(self.ENCRYPT_KEY_2) not in (16, 24, 32):
			raise ValueError("Key must be 16, 24, or 32 bytes")
		cipher = AES.new(self.ENCRYPT_KEY_2, AES.MODE_ECB)
		return cipher.decrypt(data)

	def save_snaps(self, snap_id):
		if(snap_id["id"].endswith("s")):
			return
		time = self.get_time()
		req_token = self.request_token(self.AUTH_TOKEN, time)
		r = requests.post(self.URL_BASE + "/ph/blob", data={
	    "req_token": req_token,
	    "timestamp": time,
	    "username": self.USERNAME,
	    "id": snap_id["id"],
		}, headers={"User-agent": None})
		image = r.content
		image_decrypted = s.decrypt(image)
		f = open(snap_id["id"] + (".jpg" if snap_id["m"] == 0 else ".mp4"), 'wb')
		f.write(image_decrypted)
		f.close()


#Jan 19, 2015
# s = Snapchat()
# auth_token1 = s.login("USERNAME", "PASSWORD")
# unread_snaps =  s.get_snap_list()
# for snap in unread_snaps:
# 	s.save_snaps(snap) # Saves snaps in current directory with IDs as filenames



