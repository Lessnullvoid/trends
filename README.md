

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

**Clonar imagen del raspberry**
#1 Incertar la SD Card de la replica en la mac

#2 ejecturar el comando para buscar el sd card
>diskutil list
(en la lista va aparecer algo como: /dev/disk2 o /dev/disk1)

#3 hacer una copia de la imagen 
>sudo dd if=/dev/disk2 of=~/Desktop/raspberrypi.dmg
(recuerda revisar bien el número de disco que arroje el primer comando)

#4 cuando termine el proceso de clonación sacar expulsar el sd card.

**Borrar sd card para clonar**

#1 ejecturar el comando para buscar el sd card
>diskutil list

#2 borrar y formatear 
>sudo diskutil eraseDisk FAT32 RASPBIAN MBRFormat /dev/disk2

**Carcar imagen nueva en la tarjeta limpia**

#1 desmontar el disco
>diskutil unmountDisk /dev/disk2

#2 formatear
>sudo newfs_msdos -F 16 /dev/disk2

#3 clonar
>sudo dd if=~/Desktop/raspberrypi.dmg of=/dev/disk2

 ______________________________________________________________________________

**Ejecutar Script para trends**

#1 - navegar hasta la carpeta
>cd trends

#2 -ejecutar el script 
>sudo python trends.py

**Ejecutar Script para replica**

#1 - navegar hasta la carpeta
>cd trends

#2 -ejecutar el script 
>sudo python trensreplica.py
