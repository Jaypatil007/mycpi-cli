
create a seperate folder and using python code everything.

I want to connect to sap cpi api which allows us to interact with integration contatint.

for that create few commands which will have commands like below

list package: 

can refer to this python snippet:

import requests

url = "https://3af31ef1trial.it-cpitrial05.cfapps.us10-001.hana.ondemand.com/api/v1/IntegrationPackages"

payload = {}
headers = {
  'X-CSRF-Token': '4e56cbc15a90f02a73718bbbbc8fe8acac83d14b6b434f1bddadde1ccdddf63d1751719279489',
  'Accept': 'application/json',
  'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImprdS'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

you have give credentails.json file in this folder make use of that file to get details of url and credentails first you need to fetch csrf token take refence of below Curl to correctly fetch csrf token 

curl --location 'https://3af31ef1trial.it-cpitrial05.cfapps.us10-001.hana.ondemand.com/api/v1' \
--header 'X-CSRF-Token: Fetch' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsI'

at first you need to fetch Authorization using oauth 2 and then use it to make requests for now display whatever json response we get from api to end user.