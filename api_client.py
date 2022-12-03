import requests
import json
from pprint import pprint

url = 'http://api.achuchavo.com/fd_hourly'  
# Adding Parameters
params = dict(
    rec_start="0",
    rec_count="5",
    period="hourly"
)  
response = requests.get(url, params)  
# Getting Response in JSON
data = response.json() 
sdata = str(data)
sdata = sdata.replace("\'", "\"") 

# print(sdata)
pprint(json.dumps(json.loads(sdata), sort_keys=True, indent=4, separators=(',', ': ')))
