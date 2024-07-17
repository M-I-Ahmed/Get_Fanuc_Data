import paho.mqtt.client as mqtt
from datetime import datetime
import time
import json

from Read_Robot_Data import FanucReaderCSV, FanucReaderRPI
import Calc_Robot_Indices as ri

class RobotOperation:
    UPDATE_TIME = 1

    def __init__(self, rpi=True):
        # Get the fanuc reader
        self.fanuc_reader = FanucReaderRPI(
            robot_model="Fanuc",
            host="127.0.0.1",
            port=18736,
            ee_DO_type="RDO",
            ee_DO_num=7,
        )
        self.previous_cost = 0
        self.previous_time = -1
        self.previous_velocity = None
        self.previous_reading = None

        # self.mqtt_client = mqtt.Client()
        # self.mqtt_client.connect("localhost", 1883, 60)

    def perform_calculations(self):
        update_time = time.time()
        while True:
            # Compute fields
            current_datetime  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            current_time      = time.time()
            current_reading   = self.fanuc_reader.get_next_reading()

            # Print current readings
            print(f"Time: {current_datetime}")

            #print(f"Current Reading: {current_reading}")
            current_X = current_reading.get('X', None)
            current_Y = current_reading.get('Y', None)
            current_Z = current_reading.get('Z', None)

            print(f"current_X = {current_X}")
            print(f"current_y = {current_Y}")
            print(f"current_z = {current_Z}")

            if self.previous_time != -1:
                dt = current_time - self.previous_time

                current_velocity = ri.compute_velocity(self.previous_reading, current_reading, dt)
                current_acceleration = ri.compute_acceleration(self.previous_velocity, current_velocity, dt)
                cost = ri.compute_energy_cost(current_reading, self.previous_cost, dt)

                # Print computed values
                print(f"Velocity: {current_velocity}")
                print(f"Acceleration: {current_acceleration}")
                print(f"Energy Cost: {cost}")

                # #payload = {
                #     "timestamp": current_datetime,
                #     "velocity": current_velocity,
                #     "acceleration": current_acceleration,
                #     "energy_cost": cost
                # }
                #self.mqtt_client.publish("sensor/data", json.dumps(payload))

                # Update the previous values
                self.previous_velocity = current_velocity
                self.previous_cost += cost['cost']

            print("-" * 40)

            # Sleep to maintain the update interval
            time.sleep(self.UPDATE_TIME)
            self.previous_time = current_time
            self.previous_reading = current_reading

if __name__ == '__main__':
    robot_operation = RobotOperation(rpi=True)
    robot_operation.perform_calculations()
