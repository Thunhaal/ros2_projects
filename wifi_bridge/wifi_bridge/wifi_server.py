import socket
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class WiFiServer(Node):

    def __init__(self):
        super().__init__('wifi_server')

        self.publisher = self.create_publisher(
            String,
            '/wifi_data',
            10
        )

        HOST = '0.0.0.0'
        PORT = 5000

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.server.listen(1)

        self.get_logger().info("Waiting for ESP32...")

        self.client, addr = self.server.accept()

        self.get_logger().info(f"Connected: {addr}")

        self.timer = self.create_timer(
            0.05,
            self.receive_data
        )

    def receive_data(self):

        try:

            data = self.client.recv(1024).decode().strip()

            if data:

                msg = String()
                msg.data = data

                self.publisher.publish(msg)

                self.get_logger().info(data)

        except:
            pass


def main(args=None):

    rclpy.init(args=args)

    node = WiFiServer()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
