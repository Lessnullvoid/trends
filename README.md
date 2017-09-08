# Descripción del sistema
Utilizando una camara webcam se programo un sensor que puede identificar actividad en un reticula de 3X3
De acuerdo a una logica de presencia dispara elementos audivisuales.
Cuando no detecta presencia muestra la actividad del feed de googel trends segun regiones especificas.

# Configuración de librerias
La primera parte de este tutorial contiene una lista de las librearias instaladas para hacer funcionar el sistema. En el repositorio incluimos una imagen de raspberry con todas las dependencias instaladas, pero en caso de querer iniciar una instalación desde cero aquí se incluye la lista completa.

**Librerias y dependencies**

>sudo apt-get install python-pandas

>sudo pip install beautifulsoup4

>sudo pip install requests

>sudo pip install lxml

>sudo pip install pyglet

>sudo pip install pytrends

**install opencv2**
para hacer la instalación de computer vision seguir este tutorial completo:
http://www.pyimagesearch.com/2015/02/23/install-opencv-and-python-on-your-raspberry-pi-2-and-b/

 ______________________________________________________________________________


**LIBRERIAS PARA INSTALAR ANTES DE USAR**

A pesar de ya estar instaladas se recomienda hacer una segunda instalación de estas librerias

1 - instalar esta versión de pytrends

> pip install pytrends

2 - instalar pyosc

> pip install python-osc

 ______________________________________________________________________________

# Preparación de una imagen de raspberry pi  

**Clonar imagen del raspberry al escritorio de la mac**
1. Incertar la SD Card con el sistema operativo funcional en la mac

2. ejecturar el comando para buscar el sd card
> diskutil list

_(en la lista va aparecer algo como: /dev/disk2 o /dev/disk1)_

3. hacer una copia de la imagen
> sudo dd if=/dev/disk2 of=~/Desktop/raspberrypi.dmg

_(recuerda revisar bien el número de disco que arroje el primer comando para hacer la copia correcta)_

4. cuando termine el proceso de clonación sacar expulsar el sd card.

_(el proceso puede tomar entre 30 y 40 minutos todo depende de la computadora)_

______________________________________________________________________________

**Borrar sd card para clonar**
1. Incertar una tarjeta nueva en la mac

2. Ejecturar el comando para buscar el sd card
> diskutil list

3. Borrar y formatear
> sudo diskutil eraseDisk FAT32 RASPBIAN MBRFormat /dev/disk2

**Cargar clon a una tarjeta limpia**

1. Desmontar el disco
> diskutil unmountDisk /dev/disk2

2. Formatear
> sudo newfs_msdos -F 16 /dev/disk2

3. Clonar
> sudo dd if=~/Desktop/raspberrypi.dmg of=/dev/disk2

 ______________________________________________________________________________
 **Cambiar el nombre de la raspberry**

1. Acceder a la raspberry por la terminal
> ssh pi@trends1.local

> pass: 1234

2. sudo raspi-config

________________________________________________________________________________
# Argumentos que aceptan los scripts

> los valores para región son CHI, IND, JPN, RUS, USA, ICE, MEX.


- trends_A acepta los argumentos

> "-i", "--img-dir",                default="./img/",            help="image dir path"

> "-s", "--snd-dir",                default="./snd/",            help="sound dir path"

> "-r", "--receiver-ip",            default="127.0.0.1",        help="receiver ip address"

> "-p", "--receiver-port",        default="10001",            help="receiver osc port"

> "-g", "--region",                default="CHI",                help="region"


- trends_B acepta los argumentos

> "-r", "--local-ip",            default="127.0.0.1",        help="local ip address"

> "-p", "--local-port",        default="10001",            help="local osc port"

________________________________________________________________________________
**Argumentos por script autorun**

- Editar el archivo /etc/rc.local con:
>  sudo nano /etc/rc.local

- Añadir al final del archivo, antes de "exit 0" una línea con el siguiente comando:
> (sleep 180; sudo python /home/pi/trends/trends_A.py -i "./img/" -s "./snd/" -r "127.0.0.1" -p "10001" -g "MEX") &
exit 0

- Ejemplo para  trends_B, cambiar ip/port):
(sleep 180; python /home/pi/trends/trends_B.py -r "127.0.0.1" -p "10001") &
exit 0

- Guardar los cambios

________________________________________________________________________________

**Apagar la raspberry a una hora especifica**

- Editar el archivo  /etc/crontab con:

> sudo nano /etc/crontab

- Agregar la siguiete linea al final del documento

> 30 19 * * * root shutdown -h now

- Guardar los cambios


_____________________________________________

# Ejecutar Script desde terminal

**trends_A.py**

1. Abrir terminal

2. navegar hasta la carpeta

>cd trends

3. Buscar ip de la raspberry

> hostname -I

4. Modificar direccion ip en el comando

5. -ejecutar el script trends_A

>sudo python /home/pi/trends/trends_A.py -i "./img01/" -s "./snd01/" -r "127.0.0.1" -p "10001" -g "CHI"

>sudo python /home/pi/trends/trends_A.py -i "./img02/" -s "./snd02/" -r "127.0.0.1" -p "10001" -g "CHI"

>sudo python /home/pi/trends/trends_A.py -i "./img03/" -s "./snd03/" -r "127.0.0.1" -p "10001" -g "RUS"

>sudo python /home/pi/trends/trends_A.py -i "./img04/" -s "./snd04/" -r "127.0.0.1" -p "10001" -g "CHI"

>sudo python /home/pi/trends/trends_A.py -i "./img05/" -s "./snd05/" -r "127.0.0.1" -p "10001" -g "IND"

>sudo python /home/pi/trends/trends_A.py -i "./img06/" -s "./snd06/" -r "127.0.0.1" -p "10001" -g "MEX"

>sudo python /home/pi/trends/trends_A.py -i "./img07/" -s "./snd07/" -r "127.0.0.1" -p "10001" -g "JPN"

>sudo python /home/pi/trends/trends_A.py -i "./img08/" -s "./snd08/" -r "127.0.0.1" -p "10001" -g "USA"

>sudo python /home/pi/trends/trends_A.py -i "./img09/" -s "./snd09/" -r "127.0.0.1" -p "10001" -g "ICE"




En este paso es importante modificar la dirección de ip con la dirección de la raspberry replica.

5. detener el scripts
>ctrl + c


**trends_B.py**

1. Acceder a la raspberry por la terminal
> ssh pi@trends1.local

> pass: 1234

2. navegar hasta la carpeta
>cd trends

3. ejecutar el script
>sudo python /home/pi/trends/trends_B.py -r "127.0.0.1" -p "10001"

4. detener el script
>ctrl + c

**Contenido de las carpetas de medios**

img:

img01 = Chile

img02 = Chile

img03 = Rusia

img04 = Chile

img05 = Indonesia

img06 = Mexico

img07 = Japon

img08 = EEUU

img09 = Islandia

snd:

snd01 = Chile

snd02 = Chile

snd03 = Rusia

snd04 = Chile

snd05 = Indonesia

snd06 = Mexico

snd07 = Japon

snd08 = EEUU

snd09 = Islandia

 ______________________________________________________________________________
**Actualizar el código desde el repositorio**

1. Acceder a la raspberry por la terminal
> ssh pi@trends1.local

> pass: 1234

2. Navegar hasta la carpeta
>cd trends

3. Actualizar el código con el siguiente comando
> git pull origin

 ______________________________________________________________________________
**Apagar - reboot**

> sudo shutdown -h now

> sudo reboot -h now

______________________________________________________________________________
**Mostrar IP**

> sudo ip addr show

______________________________________________________________________________
**Iniciar Teclado virtual**

> matchbox-keyboard

_________________________________________________________________________________
**Cambiar modem wifi**

1 - Ingresar a la raspberry desde la terminal con clable de ethernet conectado desde la computadora.
una vez dentro modifica el archivo wpa_supplicant con el siguiente comando:

> sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

2 - ingresar el nombre y password de la red.

3 - reiniciar y desconectar el cable ethernet


____________________________________________
**Obtener la dirección IP de la rapsberry**

> hostname -I
