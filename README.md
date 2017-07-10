# trends


#dependencies

sudo apt-get install python-pandas

sudo pip install beautifulsoup4

sudo pip install requests

sudo pip install lxml

sudo pip install pyglet

sudo pip install pytrends


#install opencv2
http://www.pyimagesearch.com/2015/02/23/install-opencv-and-python-on-your-raspberry-pi-2-and-b/

#clonar imagen del raspberry

diskutil list

sudo dd if=/dev/disk2 of=~/Desktop/raspberrypi.dmg  (recuerda revisar bien el número de disco que arroje el primer comando)

#borra sd card para cargar nueva imagen de disco
sudo diskutil eraseDisk FAT32 RASPBIAN MBRFormat /dev/disk2

#Carcar imagen nueva en la tarjeta limpia

#1 desmontar el disco
diskutil unmountDisk /dev/disk2

#2 formaterar
sudo newfs_msdos -F 16 /dev/disk2

#3 clonar
sudo dd if=~/Desktop/raspberrypi.dmg of=/dev/disk2


#ejecutar Script para trends
sudo python trends.py


#ejecutar Script para replica
sudo python trensreplica.py
