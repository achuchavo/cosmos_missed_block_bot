import requests
import json
import pprint

url = 'https://evmos-api.polkachu.com/cosmos/staking/v1beta1/validators/evmosvaloper1nfx47fqnqpcarqwt7qn4fk0llc57vvh3wgg35c/delegations'
# Adding Parameters
params = dict(
    height=12899771
)
response = requests.get(url, params)
# Getting Response in JSON
data = response.json()
print(data['delegation_responses'])
print(len(data))

# print(data[0])
for responses in data:
    print(type(responses))

# json_str = json.dumps(data)
# pprint.pprint(json.loads(json_str))
