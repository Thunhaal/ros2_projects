import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import serial


class ESP32Node(Node):

    def __init__(self):

        super().__init__('esp32_node')

        self.publisher_ = self.create_publisher(
            Float32,
            '/ultrasonic',
            10
        )

        self.ser = serial.Serial(
            '/dev/ttyACM0',
            115200,
            timeout=1
        )

        self.timer = self.create_timer(
            0.05,
            self.read_serial
        )

        self.get_logger().info("Ultrasonic Publisher Started")

    def read_serial(self):

        if self.ser.in_waiting:

            try:

                data = self.ser.readline().decode().strip()

                distance = float(data)

                msg = Float32()
                msg.data = distance

                self.publisher_.publish(msg)

                self.get_logger().info(
                    f"Distance: {distance:.2f} cm"
                )

            except ValueError:
                pass


def main(args=None):

    rclpy.init(args=args)

    node = ESP32Node()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
