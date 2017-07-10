

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

>diskutil list

>sudo dd if=/dev/disk2 of=~/Desktop/raspberrypi.dmg  (recuerda revisar bien el número de disco que arroje el primer comando)

**Borrar sd card para cargar nueva imagen de disco**
>sudo diskutil eraseDisk FAT32 RASPBIAN MBRFormat /dev/disk2

**Carcar imagen nueva en la tarjeta limpia**

#1 desmontar el disco
>diskutil unmountDisk /dev/disk2

#2 formaterar
>sudo newfs_msdos -F 16 /dev/disk2

#3 clonar
>sudo dd if=~/Desktop/raspberrypi.dmg of=/dev/disk2

 ______________________________________________________________________________

**Ejecutar Script para trends**
>sudo python trends.py

**Ejecutar Script para replica**
>sudo python trensreplica.py
