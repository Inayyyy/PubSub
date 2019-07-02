

import paho.mqtt.client as mqtt
import sys
import spider


def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))
    pass


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)

def main():
    mqttc = mqtt.Client()

    # For python2.7
    #un = raw_input("Enter user name: ")
    #pw = raw_input("Enter password: ")

    # For python3.5
    un = "user2"
    pw = "456789"
    mqttc.username_pw_set(un,pw)

    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    mqttc.on_log = on_log

    mqttc.connect("localhost", 1883, 60)
    mqttc.loop_start()

    cities = ["Banning", "Phelan"]
    for city in cities:
        msg = spider.getInfoGivenInput(city)
        infot = mqttc.publish("test/AirQuality", msg, qos=2)
        infot.wait_for_publish()

    # mqttc.loop_forever()

if __name__ == '__main__':
    main()
    sys.exit(0)
