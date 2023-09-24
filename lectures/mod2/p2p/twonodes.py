#!/usr/bin/env python3

from pythonp2p import Node
import time

class SimpleNode(Node):
    def on_message(self, data, sender, private):
      print(f"Node {self.name} received {data} from {sender}")


node0 = SimpleNode("127.0.0.1", 65430, 65432)
node1 = SimpleNode("127.0.0.2", 65431, 65433)

node0.start()
node1.start()

node0.connect_to("127.0.0.2", 65431)
node1.connect_to("127.0.0.1", 65430)


node0.send_message("Hello, how are you?")
node1.send_message("I am good, thank you.")

node0.stop()
node1.stop()