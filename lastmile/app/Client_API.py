import requests
import json

def demoTest(data):
    #funzione client che opera con API Demo
    #prendendo in input il numero delle consegne che
    #rispettivamete gli shippers effettueranno
    url='http://127.0.0.1:8000/api/demo'
    headers = {'content-type': 'application/json'}
    
    print("Loading...\n")
    response=requests.post(url, json.dumps(data), headers=headers)
    if response.status_code == 200:
        ris=json.loads(response.content.decode('utf-8'))
        return ris
    else:
        return response

def no_optimizationTest(inputJSON):
    #funzione client che opera con API No_Optimization
    #prendendo in input una strttura json corretamente composta
    url='http://127.0.0.1:8000/api/no-optimization'
    headers = {'content-type': 'application/json'}
            
    print("Loading...\n")
    response=requests.post(url, json.dumps(inputJSON), headers=headers)
    if response.status_code == 200:
        ris=json.loads(response.content.decode('utf-8'))
        return ris
    else:
        return response

def optimizationTest(inputJSON):
    #funzione client che opera con API Optimization
    #prendendo in input una struttura json corretamente composta
    url='http://127.0.0.1:8000/api/optimization'
    headers = {'content-type': 'application/json'}
        
    print("Loading...\n")
    response=requests.post(url, json.dumps(inputJSON), headers=headers)
    if response.status_code == 200:
        ris=json.loads(response.content.decode('utf-8'))
        return ris
    else:
        return response  
