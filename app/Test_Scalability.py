from Client_API import *
import json

def main():
    pathDir="C:/Users/Matteo/Desktop/Test/RUN"
    dir=1
    while dir<=5:
        pathDir="C:/Users/Matteo/Desktop/Test/RUN"+str(dir)+"/"
        i=2
        while i<=10:
            print("RUN: "+str(dir)+"  i: "+str(i))
            v=run(i, i)
            j1=json.dumps(v[0])
            j2=json.dumps(v[1])
            s="["+j1+","+j2+"]"
            f=open(pathDir+"input"+str(i)+str(i)+".json","w")
            f.write(s)
            f.close()  
            response=optimizationTest(json.loads(s))
            ris="["+json.dumps(response)+"]"
            f2=open(pathDir+"result"+str(i)+str(i)+".txt","w")
            f2.write(ris)
            f2.close()
            i=i+1
        dir=dir+1

    print("END")

main()
