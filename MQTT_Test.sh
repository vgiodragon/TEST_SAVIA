#!/bin/bash
#tiempo=0.25 #segundos

python3 suscribeAndSave.py &
sleep 2
suscriber=$!

nalarms=$1
ntest=$2

echo  "Seguro de realizar el $ntest MQTTCEPtest con $nalarms alarms [Y/n]"
read sure

if  [ "$sure" = "Y" ] || [ "$sure" = "y" ]
then
    echo "Ejecutando simulador ${nalarms}_${ntest}"
    python3 SimMQTTandSave.py $nalarms
    mhora=$(date +%H:%M:%S.)
    echo "Fin Simulacion $mhora"
    mongoexport --db savia --collection alarmaCERO --type=csv --out mqttcep/${nalarms}_${ntest}.csv --fields Vic_date,Agre_date,dateStore
    python3 dropDatabase.py
fi

kill $suscriber
#python3 SimMQTTandSave.py $ntest


