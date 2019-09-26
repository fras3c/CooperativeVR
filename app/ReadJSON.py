import json

def readFileJSON(pathFile):
    #legge il file JSON e lo restituisce sotto forma
    #di lista di stringhe
    file=open(pathFile, 'r')
    s=""
    myList=[]
    while True:
        line=file.readline().rstrip()
        if line== "":
            break
        if line == "{":
            s=line
        if line !="{":
            s=s+line
        if line =="}":
            myList.append(s)
            s=""
            continue
        if line[len(line)-1:len(line)]=="}":
            myList.append(s)
            s=""
    return myList

def fileToJSON(path):
    #dalla liste di stringhe, mi restituisce i dati
    #in modo json dai cui estrarre i dati specifici
    listJSON=[]
    listDati=readFileJSON(path)
    for i in listDati:
        j=json.loads(i)
        listJSON.append(j)  
    return listJSON


# deposito = (38.926, 16.4857)

# clienti = {0: deposito}
# clienti[IDcliente] = (lats[i], lons[i])

def extract(line):
    #trasforma la stringa di lat e lon in dati float
    new=line.replace("(","").replace(")","").split(",")
    lat,lon=float(new[0]), float(new[1])
    return lat,lon

def jsonToStructure(listJ):
    #dalla lista di dati JSON mi restituisce la struttura dati
    #sottoforma di oggetti che il sistema AlgPrototipo è in grado di analizzare
    if len(listJ) == 0:
        return "File non conforme"
    clienti1={0: (extract(listJ[0]['pos'][0]['0']))}
    noc1=listJ[0]['noc']
    x=1
    iterazioni=0
    while iterazioni<noc1-1:
        line=listJ[0]['pos'][0][str(x)]
        lat,lon=extract(line)
        clienti1[x]=(lat, lon)
        iterazioni+=1
        x+=1

    clienti2={0: (extract(listJ[1]['pos'][0]['0']))}
    iterazioni=0
    noc2=listJ[1]['noc']
    while iterazioni<noc2-1:
        line=listJ[1]['pos'][0][str(x)]
        lat,lon=extract(line)
        clienti2[x]=(lat, lon)
        iterazioni+=1
        x+=1
    return [clienti1,clienti2,noc1,noc2]

def analyzeFile(pathFile):
    #il metodo incorpora tutto il processo di conversione
    #da utilizzare all'esterno di questo file
    try:
        jsonList=fileToJSON(pathFile)
        structure=jsonToStructure(jsonList)
        return structure
    except: 
        return "File non conforme"
