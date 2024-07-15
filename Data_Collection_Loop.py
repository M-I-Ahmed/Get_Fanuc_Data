#This script will run an operation and do some calculations
#Will calculate cumulative cost, velocity and acceleration

from datetime import datetime
import time

from Read_Robot_Data import FanucReaderCSV, FanucReaderRPI
import Calc_Robot_Indices as ri

# Some constant parameters
UPDATE_TIME = 1

def main(rpi=True):
    # Get the fanuc reader
    fanuc_reader = FanucReaderRPI(
    robot_model="Fanuc",
    host="127.0.0.1",
    port=18736,
    ee_DO_type="RDO",
    ee_DO_num=7,
)

    previous_cost = 0
    previous_time, previous_velocity = -1, None
    update_time = time.time()

    while True:
        # Compute fields
        current_datetime  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current_time      = time.time()
        current_reading   = fanuc_reader.get_next_reading()

        # Print current readings
        print(f"Time: {current_datetime}")
        print(f"Current Reading: {current_reading}")

        if previous_time != -1:
            dt = current_time - previous_time

            current_velocity = ri.compute_velocity(previous_reading, current_reading, dt)
            current_acceleration = ri.compute_acceleration(previous_velocity, current_velocity, dt)
            cost = ri.compute_energy_cost(current_reading, previous_cost, dt)
    

            # Print computed values
            print(f"Velocity: {current_velocity}")
            print(f"Acceleration: {current_acceleration}")
            print(f"Energy Cost: {cost}")

            # Update the previous values
            previous_velocity = current_velocity
            previous_cost += cost['cost']

        print("-" * 40)

        # Sleep to maintain the update interval
        time.sleep(UPDATE_TIME)
        previous_time = current_time
        previous_reading = current_reading

if __name__=='__main__':
    main(rpi=True)
