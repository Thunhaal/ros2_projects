import rclpy
from rclpy.node import Node
import serial

class MotorSpeedNode(Node):

    def __init__(self):
        super().__init__('motor_speed_node')

        # Change this if your ESP32 is on a different port
        self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

        self.get_logger().info("Motor Speed Node Started")

        while rclpy.ok():

            speed = input("Enter Speed (0-100): ")

            try:
                speed = int(speed)

                if 0 <= speed <= 100:
                    self.ser.write(f"{speed}\n".encode())
                    print(f"Sent: {speed}%")
                else:
                    print("Enter value between 0 and 100")

            except ValueError:
                print("Invalid Input")

def main(args=None):
    rclpy.init(args=args)
    node = MotorSpeedNode()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
