# Get_Fanuc_Data
A Repository to enable continous collection of operational data from a Fanuc Robot.

# Important 
This repository makes use of the a slightly modified version of the fanucpy Github Repository to facilitate communication and data retrieval from the robot.

The Robot used to test this was a Fanuc ER-4iA (Educational Cell) with an R-30iB Mate Plus Controller. 

# Software Contents
The software contains two main elements
1) Fanuc Python API [(fanucpy)] https://github.com/M-I-Ahmed/fanucpy_updated - To enable the communication with the robot. 
2) The Data Collection - A Python Loop that queries the robot's state every second and prints the results out to the terminal. This loop relies on the Read_Robot_Data Script to interact with the robot and retrieve the required data, and the Calc_Robot_Indices to use the data to make some calculations and include these as outputs of the loop.  

# Driver Installation
Follow the installation instructions for the driver as detailed in the following [guide](https://github.com/torayeff/fanucpy/blob/main/fanuc.md). 

# Use Case
Once the driver has been installed on the robot, start the Mappdk_logger program. This allows the API to interact with the robot. Change the IP address in the Data_Collection_Loop script to match that of the robot. Once the python script is started, the data requested from the loop will be visible in the terminal window. 

If you want to run the Mappdk_logger alongside a normal Teach Pendant Program the MappDK_Logger needs to be called at the start of the program using the Fanuc Multitasking functionalities. 

# Modifying The Loop 
The Data_Collection_Loop.py relies on the Calc_Robot_Indices.py and Read_Robot_Data.py scripts to decide on the type of data that will be generated and retrieved. The data collection loops calls on functions from these scripts to output the data. For our use case the data that was retrieved from the script was what was needed but feel free to change the scripts to suit your needs. 

# Run.py
This file showcases an example of how the fanucpy interface is being used to manipulate the robot alongside the Data Collection Loop to retrieve the robot's operational data. 
