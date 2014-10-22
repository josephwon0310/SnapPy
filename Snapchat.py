import sys
import hashlib
import json
import requests
import time

URL_BASE = "https://feelinsonice.appspot.com"
STATIC_TOKEN = "m198sOkJEn37DjqZ32lpRu76xmw288xSQ9"
ENCRYPT_KEY_2 = "M02cnQ51Ji97vwT4"
REQ_TOKEN_PATTERN = "0001110111101110001111010101111011010001001110011000110001000110"
REQ_TOKEN_SECRET = "iEk21fuwZApXlz93750dmW22pw389dPwOk"
USERNAME = ""

def request_token(auth_token, timestamp):
    first = hashlib.sha256(REQ_TOKEN_SECRET + auth_token).hexdigest()
    second = hashlib.sha256(str(timestamp) + REQ_TOKEN_SECRET).hexdigest()
    bits = [first[i] if c == "0" else second[i] for i, c in enumerate(REQ_TOKEN_PATTERN)]
    return "".join(bits)

def get_time():
	return str(time.time())[:10]

def login(username, password):
	global USERNAME
	USERNAME = username
	time = get_time()
	req_token = request_token(STATIC_TOKEN, time)
	r = requests.post(URL_BASE + "/bq/login", data={
    "req_token": req_token,
    "timestamp": time,
    "username": username,
    "password": password
	}, headers={"User-agent": None})
	auth_token, username = r.json()["auth_token"], r.json()["username"]
	return auth_token

def get_snap_list(auth_token):
	time = get_time()
	req_token = request_token(auth_token, time)
	r = requests.post(URL_BASE + "/bq/updates", data={
    "req_token": req_token,
    "timestamp": time,
    "username": USERNAME,
	}, headers={"User-agent": None})
	unread_snaps = []
	for jsonObject in r.json()["snaps"]:
		if(jsonObject["st"] == 1 and jsonObject["id"].endswith("r")):
			unread_snaps.append(jsonObject["id"] + " img" if jsonObject["m"] == 0 else " vid")
	return unread_snaps

#def get_snaps(unread_snaps):



auth_token1 = login("UsmannK", "R6t40xxla3!")
unread_snaps =  get_snap_list(auth_token1)
for snap in unread_snaps:
	print snap
#print json.dumps(get_snap_list(), sort_keys=True, indent=4, separators=(',', ': '))





