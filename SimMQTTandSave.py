import paho.mqtt.publish as publish
import json
import datetime
from time import sleep
import _thread
import time
import sys
server     = "190.119.193.201"
#server = "localhost"
myauth = {'username':"Raspberry", 'password':"yrrebpsaR"}

def readAllJSONS():
    jsonsArray = []
    path_newJSONS= ""
    mjsonfile = open(path_newJSONS+"Alldata.txt", 'r')
    for line in mjsonfile: #Para cada linea del File
        mjson = json.loads(line.replace("'","\""))
        jsonsArray.append(mjson)
    return jsonsArray

def miMQTT(jsonsArray,latitude,longitudes,tanda,total):
    latitude = round(latitude+0.005*tanda,6)
    for grupo in range(0, total):#total
        _thread.start_new_thread( sendTriples,(jsonsArray[grupo*3+2], jsonsArray[grupo*3+1], jsonsArray[grupo*3],longitudes[2],longitudes[1],longitudes[0],latitude,tanda,grupo ))

def sendTriples(jsonsArray3_2,jsonsArray3_1,jsonsArray3,longitude2,longitude1,longitude,latitude,mtanda,grupo):
    enviar(jsonsArray3_2,longitude2,latitude,2,mtanda,grupo*3+2)
    enviar(jsonsArray3_1,longitude1,latitude,1,mtanda,grupo*3+1)
    enviar(jsonsArray3,longitude,latitude,0,mtanda,grupo*3)

def publicar(topico,mensaje,server,myauth):
    try:
        publish.single(topico, mensaje, hostname=server, auth = myauth)
        ##now save!
    except Exception as e:
        print ("Excepcion de MQTT "+str(e))

def enviar(rjson,longitude,latitude,tipo,x, posi):
    data = {}
    data['imei']   = rjson['imei']
    data['imsi']   = rjson['imsi']
    data['ses_id'] = rjson['ses_id']
    data['mac']    = rjson['mac']
    data['longitude'] = round(longitude-0.002*(x%2)*pow(-1,tipo),6)
    data['latitude'] = latitude + 0.0006*x
    data['date_simulator'] = str(datetime.datetime.now())
    topico = rjson['relation']+"/"+rjson['type']
    publicar(topico, json.dumps(data), server,myauth)

def main():
    x=int(sys.argv[1]) #take first argument
    jsonsArray = readAllJSONS()
    latitude = -12.111111
    longitudes = [-76.940022, -76.951022, -76.944022]
    total = x*(1)
    print("Envio "+str(total)+" alarmas "+str(datetime.datetime.now()))
    for tanda in range(1,16):
        _thread.start_new_thread( miMQTT,(jsonsArray, latitude, longitudes, tanda, total ))
        sleep(60)
        #print("Fin "+str(datetime.datetime.now()) ) #+" total DB "+str(db.responses.count()))

if __name__ == "__main__":
    main()
