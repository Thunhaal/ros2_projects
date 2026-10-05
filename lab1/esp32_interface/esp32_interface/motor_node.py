import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import serial


class MotorNode(Node):

    def __init__(self):
        super().__init__('motor_node')

        self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

        self.subscription = self.create_subscription(
            Int32,
            '/motor_cmd',
            self.motor_callback,
            10
        )

        self.get_logger().info("Motor Node Ready")

    def motor_callback(self, msg):

        pwm = msg.data

        self.ser.write(f"{pwm}\n".encode())

        self.get_logger().info(f"PWM Sent: {pwm}")


def main(args=None):

    rclpy.init(args=args)

    node = MotorNode()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
