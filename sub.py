import paho.mqtt.client as mqtt
import os

broker = "localhost"

def on_connect(mqttc, obj, flags, rc):
    if rc==0:
        print("Connected OK Returned code = "+ str(rc))
    elif rc==5:
        print("Not Authorized Returned code = " + str(rc))
    else:
        print("Bad Connection Returned code = " + str(rc))


def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)

def main():
    mqttc = mqtt.Client()

    # For python2.7
    un = raw_input("Enter user name: ")
    pw = raw_input("Enter password: ")

    # For python3.6
    # un = input("Enter user name: ")
    # pw = input("Enter password: ")

    mqttc.username_pw_set(un,pw)

    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    mqttc.on_log = on_log

    mqttc.connect(broker, 1883, 60)

    # For python2.7
    tp = raw_input("Enter the topic you want to subscribe: ")

    # For python3.6
    # tp = input("Enter the topic you want to subscribe: ")
    mqttc.subscribe(tp, 0)

    mqttc.loop_forever()

if __name__ == '__main__':
    main()
    sys.exit(0)


