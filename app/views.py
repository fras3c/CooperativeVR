from django.shortcuts import render
from . import frasec
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse
from . import AlgPrototipo
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import ReadJSON
from django import forms



# Create your views here.


@api_view(['POST'])
def without_optimization_api(request):
    
 #   inputDati = ReadJSON.read(request.data)
  #  print(inputDati)
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
    #if request.is_ajax():
    if request.method == 'POST':
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

    return Response(value)
    #return Response(json.dumps(value))


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
lats, lons, route, cost = frasec.run()
latitudine = []
longitudine = []
for i in range(len(lats)):
    latitudine.append(lats[i])
    longitudine.append(lons[i])


value = {'lat' : latitudine, 'lon': longitudine, 'rotta' : route, 'costo' : cost}#, 'deposito': [16.48757,38.92574], 'c1':[16.692104177184746, 39.18847606525372], 'c2':[16.380523533774532, 39.181744129419634]}
'''

@csrf_exempt
def index(request):
    return render(request, 'default-table-new2.html')#

class UploadForm(forms.Form):
    file=forms.FileField()

def parseData(inputDati):
    ris = []
    nocs = []
    for shipper in inputDati:
        nocs.append(shipper['noc'])
        clienti = {}
        for cliente in shipper['pos'].items():
            clienti[int(cliente[0])] = tuple(cliente[1])
        ris.append(clienti)
    for x in nocs:
        ris.append(int(x))

    return ris

@csrf_exempt
def upload(request):
    value = {}
    if request.is_ajax():
        form=UploadForm(request.POST, request.FILES)
        if form.is_valid():
            pathFile=saveFile(request.FILES['file'])
            inputDati = None
            with open(pathFile, 'r') as f:
                inputDati = json.load(f)

            if inputDati == None:
                return HttpResponse("-1")
            #inputDati = ReadJSON.jsonToStructure(inputDati)
            #inputDati=ReadJSON.analyzeFile(pathFile)
            #if inputDati == "File non conforme":
            #    return HttpResponse("-1")

            inputDati = parseData(inputDati)             
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

def saveFile(file):
    #salvataggio file del file in input tramite caricamento
    pathFile="./app/output/myFile"
    with open(pathFile, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return pathFile

def writeFile(line):
    #salvataggio su file delle coordinate manuali in input
    pathFile="./app/output/myFile_Manual"
    f=open(pathFile, 'w')
    f.write(line)
    f.close()
    return pathFile

@csrf_exempt
def manual(request):
    value = {}
    if request.is_ajax():
        #body_unicode contiene la stringa da fare il parsing
        body_unicode = request.body.decode('utf-8')
        pathFile=writeFile(body_unicode)
        inputDati=ReadJSON.analyzeFile(pathFile) 
        if inputDati == "File non conforme":
                return HttpResponse(-1)
        
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
