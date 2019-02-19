#!/bin/bash
#tiempo=0.25 #segundos

nalarms=$1
ntest=$2

echo  "Seguro de realizar el $ntest POSTtest con $nalarms alarms [Y/n]"
read sure

if  [ "$sure" = "Y" ] || [ "$sure" = "y" ]
then
    echo "Ejecutando simulador"
    python3 sendPost.py $nalarms
    mhora=$(date +%H:%M:%S.)
    echo "Fin Simulacion $mhora"
    mongoexport --db postsavia --collection responses --type=csv --out post/${nalarms}_${ntest}.csv --fields Vic_date,dateStore

    python3 dropDatabase.py
fi

#python3 SimMQTTandSave.py $ntest
