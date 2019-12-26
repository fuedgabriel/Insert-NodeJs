import requests
import json
r = requests.get('http://one.zetai.info/api/episodioexes/3')
print(r.json)
