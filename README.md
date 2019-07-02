# Setup Broker  
### Enable Authentication
1. Create a new file named `local.conf` under directory `/etc/mosquitto/conf.d`
2. Type following two lines in `local.conf`:  
```sh
allow_anonymous false  
password_file /etc/mosquitto/passwd
```  

3. Use tool `mosquitto_passwd` to manage usernames and passwords in terminal.

# test with subscriber and publisher  
- sub.py - this is a subscriber script written in python.  
- pub.py - this is a publisher script written in python. It publishes the air quality infomation of cities in CA. Data comes from [AirNow - California Air Quality website](https://www.airnow.gov/index.cfm?action=airnow.local_state&stateid=5). 

### About Authentication
- Publishers are authenticated through user input.
- Subscribers are authenticated inside of python script.  

### Specify Topic and Cities  
`pub.py` specifies the topic and cities. Here for test, topic is `test/AirQuality`, and two cities are `Banning` and `Phelan`. When running `sub.py`, topic should be consistent with the one specified in pub.py.