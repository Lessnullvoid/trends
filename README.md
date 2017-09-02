

**Librerias y dependencies**
Estos son los programas que se tienen que instalar en la raspberry para poder hacer funcionar el software.
Por el momento el clone con el que estamos trabajando ya tiene todo instalado pero en caso de que fuera necesario hacer una instalación desde cero esto es lo que se necesita:

>sudo apt-get install python-pandas

>sudo pip install beautifulsoup4

>sudo pip install requests

>sudo pip install lxml

>sudo pip install pyglet

>sudo pip install pytrends

**install opencv2**
http://www.pyimagesearch.com/2015/02/23/install-opencv-and-python-on-your-raspberry-pi-2-and-b/

 ______________________________________________________________________________

**NUEVAS LIBRERIAS PARA INSTALAR ANTES DE USAR**

1 - instalar esta versión de pytrends

> pip install pytrends

2 - instalar pyosc

> pip install python-osc

 ______________________________________________________________________________

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

 ______________________________________________________________________________


**Ejecutar Script trends_A desde terminal raspberry**

1. Abrir terminal

2. Iniciar teclado virtual

> matchbox-keyboard

3. navegar hasta la carpeta

>cd trends

4. Buscar ip de la raspberry

> sudo ip addr show

5. Modificar direccion ip en cada documento

6. -ejecutar el script trends_B  
>sudo python trends_B.py

6. -ejecutar el script trends_A  
>sudo python trends_A.py

5. detener el scripts
>ctrl + c


**Ejecutar Script para replica desde terminal mac**

1. Acceder a la raspberry por la terminal
> ssh pi@trends1.local

> pass: 1234

2. navegar hasta la carpeta
>cd trends

3. iniciar la pantalla externa
> export DIPLAY=:10.0

4. ejecutar el script
>sudo python trensreplica.py

5. detener el script
>ctrl + c

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

________________________________________________________________________________
**Argumentos por programa**

- trends_A acepta los argumentos

> "-i", "--img-dir",                default="./img/",            help="image dir path"

> "-s", "--snd-dir",                default="./snd/",            help="sound dir path"

> "-r", "--receiver-ip",            default="127.0.0.1",        help="receiver ip address"

> "-p", "--receiver-port",        default="10001",            help="receiver osc port"

> "-g", "--region",                default="CHI",                help="region"

los valores para región son CHI, IND, JPN, RUS, USA, ICE, MEX.

- trends_B acepta los argumentos

> "-r", "--local-ip",            default="127.0.0.1",        help="local ip address"

> "-p", "--local-port",        default="10001",            help="local osc port"

________________________________________________________________________________
**Argumentos por script autorun**

# Editar el archivo /etc/rc.local con:
$ nano /etc/rc.local

# Añadir al final del archivo, antes de "exit 0" una línea con el siguiente comando:
# (Ejemplo para  trends_A, región México, cambiar path, directorios e ip/port):
(sleep 180; sudo python /home/pi/trends/trends_A.py -i "./img/" -s "./snd/" -r "127.0.0.1" -p "10001" -g "MEX") &
exit 0

# (Ejemplo para  trends_B, cambiar ip/port):
(sleep 180; python /home/pi/trends/trends_B.py -r "127.0.0.1" -p "10001") &
exit 0

_____________________________________________
**Cambiar modem wifi**

> sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

____________________________________________
**Obtener la dirección IP de la rapsberry**

> hostname -I
