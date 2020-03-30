import re

text = ["http://127.0.0.1:5454/author/de305d54-75b4-431b-adb2-eb6b9e546013",
		"http://127.0.0.1:5454/author/ae345d54-75b4-431b-adb2-fb6b9e547891",]

for t in text:
    r = re.findall(r"(https?://[-A-Za-z0-9+&@#%?=~_|!:,.;]+/)author/([-A-Za-z0-9]+)/?", t, re.I)
    uid = r[0][1]
    print(uid)