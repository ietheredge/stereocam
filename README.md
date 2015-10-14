# onpiboot
#Housekeeping scripts to perform at start up of raspberrypi. these scripts are run (in Raspbian)

#You may need to:
sudo chmod +x startup_mailer.py

#and in order to run this it start up edit:
sudo nano /etc/rc.local
#add

 _IP=$(hostname -I) || true  
 if [ "$_IP" ]; then  
   printf "My IP address is %s\n" "$_IP"  
   python  [path to folder]/startup_mailer.py        <<<--THIS LINE!!!  
 fi  
 exit 0   
 
#The data used in is stored in two places in two places in the root folder. less sensitive stuff in a config file (.ini) the more sensitive stuff in the netrc file (/.netrc)

#config file should be formatted like this:
[Settings]  
hostname: [your email host name, eg: smtp.gmail.com]  
toaddress: [emailaddress you want to send to]  
compname: [the name of your machine eg: RaspberryPi]  
#and... the netrc
machine [your email host] login [fred] password [bluebonnet]  

