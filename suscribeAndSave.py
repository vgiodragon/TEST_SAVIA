import paho.mqtt.client as mqtt
import threading
from pymongo import MongoClient
import json
import datetime

clientMongo = MongoClient()
db = clientMongo.savia

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    nmsg = str(msg.payload, 'utf-8')
    try:
        mjson = json.loads(nmsg)
        if "Prevencion" in msg.topic:
            mjson['dateStore'] = str(datetime.datetime.now())
            db.alarmaPrevencion.insert_one(mjson)
        elif "CERO" in msg.topic:
            mjson['dateStore'] = str(datetime.datetime.now())
            db.alarmaCERO.insert_one(mjson)
        elif "Seguimiento" in msg.topic:
            mjson['dateStore'] = str(datetime.datetime.now())
            db.alarmaSeguimiento.insert_one(mjson)
        else:
            mjson['horaAlmacenada'] = str(datetime.datetime.now())
            db.positions.insert_one(mjson)
    except ValueError as error:
        print("exp json"+str(error))

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    username   = "CTIC-SMARTCITY"
    password   = "YTICTRAMS-CITC"
    # set username and password
    client.username_pw_set(username, password)
    client.connect("190.119.193.201", 1883, 60)
#    client.connect("localhost", 1883, 60)
    client.loop_forever()

if __name__ == "__main__":
    main()
