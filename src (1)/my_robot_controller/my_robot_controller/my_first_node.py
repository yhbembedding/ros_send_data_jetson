#!/usr/bin/env python3
import rclpy
from jtop import jtop

from rclpy.node import Node
import psutil

def secs2hours(secs):
    mm, ss = divmod(secs, 60)
    hh, mm = divmod(mm, 60)
    return "%d:%02d:%02d" % (hh, mm, ss)

class MyNode(Node):
    def __init__(self):
        super().__init__("first_node")
        self.create_timer(1.0,self.timer_callback)
    def timer_callback(self):
        # print("cpu ",psutil.cpu_percent())
        # print("Ram ",psutil.virtual_memory())
        battery = psutil.sensors_battery()
        
        with jtop() as jetson:
    # jetson.ok() will provide the proper update frequency
            if jetson.ok():
                for idx, cpu in enumerate(jetson.cpu['cpu']):
                    print("------ CPU{idx} ------".format(idx=idx))
                    for key, value in cpu.items():
                        print("{key}: {value}".format(key=key, value=value))
           
                total = jetson.cpu['total']
                print("------ TOTAL ------")
                for key, value in total.items():
                    print("{key}: {value}".format(key=key, value=value))
        # print("battery ", battery)
        # print("charge = %s%%, time left = %s" % (battery.percent, secs2hours(battery.secsleft)))
        self.get_logger().info("Timer by YHB")

def main(args = None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ =='__main__':
    main()