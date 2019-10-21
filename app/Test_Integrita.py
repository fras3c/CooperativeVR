import requests
import json


def demoTest(data):
    #funzione client che opera con API Demo
    #prendendo in input il numero delle consegne che
    #rispettivamete gli shippers effettueranno
    
    url='http://127.0.0.1:8000/api/demo'
    headers = {'content-type': 'application/json'}
    response=requests.post(url, json.dumps(data), headers=headers)
    #response=requests.put(url, json.dumps(data), headers=headers)
    print("\nCLIENT HEADERS")
    v=response.request.headers
    for i in v:
        print("\t"+i+": "+str(v[i]))
    print()
    print("RESPONSE: "+str(response))
    print(str(response.text))
    print()
    
def main():
    c={"noc1":2, "noc2":2}
    demoTest(c)
    

main()
