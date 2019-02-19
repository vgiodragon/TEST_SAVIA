Read Me:
Explicación para realizar las simulaciones de envío para las arquitecturas MQTT- CEP vs POST.

Previo:
* Desde la máquina donde se origina el envío asegurarse de que esté ejecutándose el service de mongod. En caso contrario ejecutar:
    $ sudo service mongod start
* Para conectarse a la nube con las arquitecturas mencionadas se tiene que hacer por ssh 
    ssh giodragon@190.119.193.201
cuya contraseña es: smartcity1

* Para los casos de Alarmas según test debe ser así
       # Alarmas  TOTAL
          30       210
          60       420
          90       630
          120      840
          150      1050

----------------------------------------------------------------------------------------------------------------------------
Test MQTT-CEP:
* Para este test se necesitan 3 terminales de los cuales 2 tienen que estar conectados a la nube por ssh y en el directorio $HOME/smartcitysavia

  Terminal 1 :
    $ ssh giodragon@190.119.193.201
    $ cd smartcitysavia
    $ ./paso1MQTT.sh
   Levanta el service. Limpia los  log, luego compila el proyecto, reincia el servicio de flink y finalmente ejecuta el proyecto. EL mensaje final debe decir "Starting execution of program"

  Terminal 2 :
    $ ssh giodragon@190.119.193.201
    $ cd smartcitysavia
    $ ./paso2MQTT.sh
  Almacena las info obtenida del perf. Se suscribe para almacenar en la DB los mensajes que llegan, luego pide que ingrese nombre del test se sugiere que sea en fomato #Alarmas_#test x ejm 120_6 que quiere decir 120 alarmas test # 6. Luego para primera vez pedirá la contraseña de la nube pues para ejecutar los comandos de perf es necesario acceso de root. Estará ejecutándose esa recolección de performance por 15 minutos y medio aprox. Finalmente limpia la DB.

  Terminal 3 :
    $ ./MQTT_Test.sh 120 6
  Ejecuta la simulación de envío por 15 minutos. Para ejecutar el script se necesita dos parametros de ingreso que en el formato #Alarmas #test x ejm 120 6 que quiere decir que se enviarán 120 alarmas y es test # 6. Primero se suscribe para obtener los datos de latencia. Luego pide confirmación y comienza la simulación x 15 min. Finalmente se alamacena en un file la información de la latencia de la DB para terminar limpiandola.


* Tanto para el Terminal 2 y 3 se muestran los tiempos de inicio y fin. En caso de un nuevo test al Terminal 1 se le corta el script con Ctrl+C.
* Para el caso de querer limpiar la DB en la nube ejecutar el comando python3 $HOME/smartcitysavia/DropDatabase.py
* Para el caso de querer limpiar la DB en local ejecutar el comando python3 dropDatabase.py

----------------------------------------------------------------------------------------------------------------------------
Test POST:
* Para este test se necesitan 2 terminales de los cual 1 tienen que estar conectados a la nube por ssh y en el directorio $HOME.

  Terminal 1 : 
    $ ./paso1POST.sh
  Levanta el service y almacena las info obtenida del perf. Al ejecutar pide que ingrese nombre del test se sugiere que sea en fomato #Alarmas_#test x ejm 120_6 que quiere decir 120 alarmas test # 6. Luego para primera vez pedirá la contraseña de la nube pues para ejecutar los comandos de perf es necesario acceso de root. Estará ejecutándose esa recolección de performance por 15 minutos y medio aprox. Finalmente limpia la DB.

  En caso se haga un test justo luego de hacer pruebas MQTT-CEP entonces se debe cortar el service de este último con el script stopFlink.sh ubicado en $HOME. 

  Terminal 2 :
    $ ./POST_TEST.sh 30 2
  Ejecuta la simulación de envío por 15 minutos. Para ejecutar el script se necesita dos parametros de ingreso que en el formato #Alarmas #test x ejm 120 6 que quiere decir que se enviarán 120 alarmas y es test # 6. Para cada envío tipo POST en el caso de que la respuesta http sea de alarma se alamacena en la DB local. Para termina se exporta la DB de latencia en un archivo para finalmente limpiarla.

* Para ambos terminales se muestran los tiempos de inicio y fin.
* Para el caso de querer limpiar la DB en la nube ejecutar el comando python3 $HOME/smartcitysavia/DropDatabase.py
* Para el caso de querer limpiar la DB en local ejecutar el comando python3 dropDatabase.py

