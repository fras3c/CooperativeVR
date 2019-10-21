from django.shortcuts import render
from . import frasec
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse
from . import AlgPrototipo
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

import time


#Creazioni Api

@api_view(['POST'])
def optimization_api(request):
    clienti = parseData(request.data)
    value = AlgPrototipo.cooperation(clienti[0], clienti[1])
    return Response(value)
    ''' Usato per effettuare i test di scalabilità
    temp={}
    tStartCop=time.time()*1000
    value = AlgPrototipo.cooperationScalability(clienti[0], clienti[1], temp)
    tEndCop=time.time()*1000
    temp['Tot-Esec']=(tEndCop-tStartCop)
    val=0
    for i in temp:
        if i != 'Tot-Esec':
            val=val+temp[i]
    t=temp['Tot-Esec']-val
    temp['Scamb']=t
    return Response(temp)
    '''


@api_view(['POST'])
def no_optimization_api(request):

    inputDati = parseData(request.data)
    clienti, s = AlgPrototipo.upload(inputDati)
    clienti1 = clienti[0]
    route1, cost1 = s[0]
    clienti2 = clienti[1]
    route2, cost2 = s[1]
    value = {'clienti1' : clienti1, 'clienti2' : clienti2, 'rotta1' : route1, 'costo1' : cost1, 'rotta2' : route2, 'costo2' : cost2}
    return Response(value)

@api_view(['POST'])
def demo_api(request):
    value = {}
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    noc1 = int(body['noc1'])
    noc2 = int(body['noc2'])
    clienti, s = AlgPrototipo.demo(noc1, noc2)
    clienti1 = clienti[0]
    route1, cost1 = s[0]
    clienti2 = clienti[1]
    route2, cost2 = s[1]
    value = {'clienti1' : clienti1, 'clienti2' : clienti2, 'rotta1' : route1, 'costo1' : cost1, 'rotta2' : route2, 'costo2' : cost2}
    return Response(value)
    #return Response(json.dumps(value))


#Creazione viste

@csrf_exempt
def index(request):
    return render(request, 'index.html')


@csrf_exempt
def demo(request):
    value = {}
    if request.is_ajax():
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        noc1 = int(body['noc1'])
        noc2 = int(body['noc2'])

        print("Noc1", noc1)
        print("Noc2", noc2)

        clienti, s = AlgPrototipo.demo(noc1, noc2)
        clienti1 = clienti[0]
        route1, cost1 = s[0]

        #{0: (38.926, 16.4857), 1: (39.283913942532216, 16.434401280765925), 2: (39.05523863247818, 16.734295616438725), 3: (39.12481454466452, 16.669553003984852), 4: (39.27000123068061, 16.56065906064284), 5: (39.095311778709615, 16.34893874124117), 6: (39.00022937302457, 16.936617650408916), 7: (39.19007651998094, 16.316824079328395), 8: (39.242581105056914, 16.732473096255326), 9: (39.03409314993345, 16.872463600090224), 10: (39.04454422881649, 16.700485401090827)}

        clienti2 = clienti[1]
        route2, cost2 = s[1]
        #value = {'lat1' : latitudine1, 'lon1': longitudine1, 'rotta1' : route1, 'costo1' : cost1, 'lat2' : latitudine2, 'lon2': longitudine2, 'rotta2' : route2, 'costo2' : cost2} #, 'deposito': [16.48757,38.92574], 'c1':[16.692104177184746, 39.18847606525372], 'c2':[16.380523533774532, 39.181744129419634]}
        value = {'clienti1' : clienti1, 'clienti2' : clienti2, 'rotta1' : route1, 'costo1' : cost1, 'rotta2' : route2, 'costo2' : cost2}
        print(value)
    else:
        print('no')

    return HttpResponse(json.dumps(value), content_type='application/json')


@csrf_exempt
def cooperation(request):
    value = {}

    if request.is_ajax():
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        if len(body) < 2:
            return HttpResponse(json.dumps(value), content_type='application/json')

        clienti1 = {int(k): v for k,v in body['clienti1'].items()}
        clienti2 = {int(k): v for k,v in body['clienti2'].items()}
        #print(clienti1)
        #print(clienti2)
        value = AlgPrototipo.cooperation(clienti1, clienti2)
        print(value)
        '''
        lat = body['lat']
        lon = body['lon']
        rotta = body['rotta']
        print("Lats:", lat)
        print("Lons:", lon)
        print("Rotta:", rotta)
        '''
        #print("Risultati:", route1, route2, s1opt, s2opt)

    return HttpResponse(json.dumps(value), content_type='application/json')

@csrf_exempt
def upload(request):
    value = {}

    if request.is_ajax():
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
    
        inputDati = parseData(body)          
        clienti, s = AlgPrototipo.upload(inputDati)
        clienti1 = clienti[0]
        route1, cost1 = s[0]

         #{0: (38.926, 16.4857), 1: (39.283913942532216, 16.434401280765925), 2: (39.05523863247818, 16.734295616438725), 3: (39.12481454466452, 16.669553003984852), 4: (39.27000123068061, 16.56065906064284), 5: (39.095311778709615, 16.34893874124117), 6: (39.00022937302457, 16.936617650408916), 7: (39.19007651998094, 16.316824079328395), 8: (39.242581105056914, 16.732473096255326), 9: (39.03409314993345, 16.872463600090224), 10: (39.04454422881649, 16.700485401090827)}

        clienti2 = clienti[1]
        route2, cost2 = s[1]
        #value = {'lat1' : latitudine1, 'lon1': longitudine1, 'rotta1' : route1, 'costo1' : cost1, 'lat2' : latitudine2, 'lon2': longitudine2, 'rotta2' : route2, 'costo2' : cost2} #, 'deposito': [16.48757,38.92574], 'c1':[16.692104177184746, 39.18847606525372], 'c2':[16.380523533774532, 39.181744129419634]}
        value = {'clienti1' : clienti1, 'clienti2' : clienti2, 'rotta1' : route1, 'costo1' : cost1, 'rotta2' : route2, 'costo2' : cost2}
        print(value)
    else:
        print('no')
    return HttpResponse(json.dumps(value), content_type='application/json')

@csrf_exempt
def manual(request):
    value = {}
    if request.is_ajax():
        #body_unicode contiene la stringa da fare il parsing
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        inputDati = parseData(body)
        print(inputDati)
        clienti, s = AlgPrototipo.upload(inputDati)
        clienti1 = clienti[0]
        route1, cost1 = s[0]

        #{0: (38.926, 16.4857), 1: (39.283913942532216, 16.434401280765925), 2: (39.05523863247818, 16.734295616438725), 3: (39.12481454466452, 16.669553003984852), 4: (39.27000123068061, 16.56065906064284), 5: (39.095311778709615, 16.34893874124117), 6: (39.00022937302457, 16.936617650408916), 7: (39.19007651998094, 16.316824079328395), 8: (39.242581105056914, 16.732473096255326), 9: (39.03409314993345, 16.872463600090224), 10: (39.04454422881649, 16.700485401090827)}

        clienti2 = clienti[1]
        route2, cost2 = s[1]
        #value = {'lat1' : latitudine1, 'lon1': longitudine1, 'rotta1' : route1, 'costo1' : cost1, 'lat2' : latitudine2, 'lon2': longitudine2, 'rotta2' : route2, 'costo2' : cost2} #, 'deposito': [16.48757,38.92574], 'c1':[16.692104177184746, 39.18847606525372], 'c2':[16.380523533774532, 39.181744129419634]}
        value = {'clienti1' : clienti1, 'clienti2' : clienti2, 'rotta1' : route1, 'costo1' : cost1, 'rotta2' : route2, 'costo2' : cost2}
        print(value)
    else:
        print('no')
    return HttpResponse(json.dumps(value), content_type='application/json')



'''
@csrf_exempt
def solve(request):
    value = {}
    if request.is_ajax():
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        noc1 = int(body['noc1'])
        noc2 = int(body['noc2'])

        print("Noc1", noc1)
        print("Noc2", noc2)

        lats1, lons1, route1, cost1 = frasec.run(noc1)
        latitudine1 = []
        longitudine1 = []
        for i in range(len(lats1)):
            latitudine1.append(lats1[i])
            longitudine1.append(lons1[i])

        lats2, lons2, route2, cost2 = frasec.run(noc2)
        latitudine2 = []
        longitudine2 = []
        for i in range(len(lats2)):
            latitudine2.append(lats2[i])
            longitudine2.append(lons2[i])

        print(latitudine1)
        print(longitudine1)
        print(latitudine2)
        print(longitudine2)


        value = {'lat1' : latitudine1, 'lon1': longitudine1, 'rotta1' : route1, 'costo1' : cost1, 'lat2' : latitudine2, 'lon2': longitudine2, 'rotta2' : route2, 'costo2' : cost2} #, 'deposito': [16.48757,38.92574], 'c1':[16.692104177184746, 39.18847606525372], 'c2':[16.380523533774532, 39.181744129419634]}

    else:
        print('no')

    return HttpResponse(json.dumps(value), content_type='application/json')

@csrf_exempt
def demobak(request):
    value = {}
    if request.is_ajax():
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        name = body['FileName']
        print("ciaociao " +name)

        lats, lons, route, cost = frasec.run(10)
        latitudine = []
        longitudine = []
        for i in range(len(lats)):
            latitudine.append(lats[i])
            longitudine.append(lons[i])

        value = {'lat' : latitudine, 'lon': longitudine, 'rotta' : route, 'costo' : cost}#, 'deposito': [16.48757,38.92574], 'c1':[16.692104177184746, 39.18847606525372], 'c2':[16.380523533774532, 39.181744129419634]}

    else:
        print('no')

    return HttpResponse(json.dumps(value), content_type='application/json')

    #return render(request, 'default.html', {'value':value})
'''
'''
lats, lons, route, cost = frasec.run()
latitudine = []
longitudine = []
for i in range(len(lats)):
    latitudine.append(lats[i])
    longitudine.append(lons[i])


value = {'lat' : latitudine, 'lon': longitudine, 'rotta' : route, 'costo' : cost}#, 'deposito': [16.48757,38.92574], 'c1':[16.692104177184746, 39.18847606525372], 'c2':[16.380523533774532, 39.181744129419634]}
'''

#Metodo utilita'

def parseData(inputDati):
    '''il metodo crea la strutta dati
    adatta per passarla in input al modulo AlgPrototipo'''
    ris = []
    for shipper in inputDati:        
        clienti = {}
        for cliente in shipper.items():
            clienti[int(cliente[0])] = tuple(cliente[1])
        ris.append(clienti)

    return ris