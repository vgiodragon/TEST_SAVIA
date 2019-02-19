import requests
import json
import _thread
import datetime
from time import sleep
from pymongo import MongoClient
import sys

clientMongo = MongoClient()
db = clientMongo.postsavia

def readAllJSONS():
    jsonsArray = []
    mjsonfile = open("Alldata.txt", 'r')
    for line in mjsonfile: #Para cada linea del File
        mjson = json.loads(line.replace("'","\""))
        jsonsArray.append(mjson)
    return jsonsArray

def miPOST(jsonsArray,latitude,longitudes,tanda,total):
    ip = 'http://190.119.193.201:8081/postData2'
    initialtime = datetime.datetime.strptime('00:00', '%H:%M') + datetime.timedelta(minutes=(total+tanda))
    hora_minutos = initialtime.strftime("%H:%M")
    latitude = round(latitude+0.005*tanda,6)
    for grupo in range(0, total):#total
        enviar(ip,jsonsArray[grupo*3+2],longitudes[2],latitude,2,hora_minutos,tanda,grupo*3+2)
        enviar(ip,jsonsArray[grupo*3+1],longitudes[1],latitude,1,hora_minutos,tanda,grupo*3+1)
        enviar(ip,jsonsArray[grupo*3],longitudes[0],latitude,0,hora_minutos,tanda,grupo*3)

def enviar(ip,rjson,longitude,latitude,tipo,hora_minutos,x, posi):
    rjson['longitude'] = round(longitude-0.002*(x%2)*pow(-1,tipo),6)
    rjson['latitude'] = latitude + 0.0006*x
    rjson['date_simulator'] = rjson['date_simulator'][:11] + hora_minutos
    data = str(rjson).replace("'","\"")
    payload = {'data': data}
    vic_date = str(datetime.datetime.now())
    r = requests.post(ip, data=payload)
    if tipo == 0 :
        mjson = r.json()
        if "response" in mjson:
            mjson['ses_id'] = "00"+str(posi+121)
            mjson['Vic_date'] = vic_date
            mjson['dateStore'] = str(datetime.datetime.now())
            db.responses.insert_one(mjson)

def main():
    x=int(sys.argv[1]) #take first argument
    server = "190.119.193.201"
    jsonsArray = readAllJSONS()
    latitude = -12.111111
    longitudes = [-76.940022, -76.951022, -76.944022]
    #for x in range (4,5):
    total = x*(1)
    print("Envio "+str(total)+" usuarios "+str(datetime.datetime.now()))
    for tanda in range(0,15):
        _thread.start_new_thread( miPOST,(jsonsArray, latitude, longitudes, tanda, total ))
        sleep(60)
    sleep(10)
    #print("Fin "+str(datetime.datetime.now()) )

if __name__ == "__main__":
    main()

