#!/usr/bin/python3

import rospy
from jtop import jtop
import requests
from std_msgs.msg import String
import json
from jetbot import Robot

def publisher():
      
    # define the actions the publisher will make
    pub = rospy.Publisher('/data_request',
                          String, queue_size=10)
    # initialize the publishing node
    rospy.init_node('send_data', anonymous=True)
      
    # define how many times per second
    # will the data be published
    # let's say 10 times/second or 10Hz
    rate = rospy.Rate(10)
    # to keep publishing as long as the core is running
    while not rospy.is_shutdown():
        data = "The data that you wish to publish."
          
              
             
        with jtop() as jetson:
        # jetson.ok() will provide the proper update frequency
            while jetson.ok():
                # Read tegra stats
                t = jetson.stats
            
                del t['time'],t['uptime']
                # print(t)
                t = json.loads(json.dumps(t))
                # print(t)
                headers = {'content-type':'application/json'}
                try:
                    msg = requests.post(url="http://192.168.0.103:5000/json",json=t,headers=headers)
                    print(msg.text)
                except:
                    print("not connection to server")
                # msfff = requests.request("POST", url="https://192.168.0.103:5000/json", data=t, headers=headers)
                # print(msfff)
    # EOF     
        # rospy.loginfo(data)
          
        # publish the data to the topic using publish()
        pub.publish(data)
          
        # keep a buffer based on the rate defined earlier
        rate.sleep()
  
    

if __name__ == '__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass
    # rospy.init_node("test_node")
    # rospy.loginfo("hello node ros")
    # rospy.sleep(1.0)
    # rospy.loginfo("end game")
    # rate = rospy.Rate(10)
    # while not rospy.is_shutdown():
    #     rospy.loginfo("aaaa")
    #     rate.sleep()
    
    
