import time
import serial
from serial.tools import list_ports
import matplotlib.pyplot as plt

ports = list_ports.comports()

file = open("data.csv", "w", newline='')
file.truncate()

serialCom = serial.Serial('COM3', 115200)

#Reset Arduino
serialCom.setDTR(False)
time.sleep(1)
serialCom.flushInput()
serialCom.setDTR(True)

#Recording Time (seconds)
timeInterval = 3600

#Enable Interactive Plotting Mode
plt.ion()

#Generate Two Separate Figures
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
fig3, ax3 = plt.subplots()

#Creating Empty Data Arrays
timeVals = []
feedSpeedVals = []
drawSpeedVals = []
predictedDiamVals = []
measuredDiamVals = []

#Create Lines
line1, = ax1.plot(timeVals, predictedDiamVals, label="Predicted Filament Diameter", color="blue")
line2, = ax1.plot(timeVals, measuredDiamVals, label="Measured Filament Diameter", color='red')
line3, = ax2.plot(timeVals, drawSpeedVals, label="Draw Speed", color='magenta')
line4, = ax3.plot(timeVals, feedSpeedVals, label="Feed Speed", color='green')

#Create Chart Legends
ax1.legend(loc='upper left')
ax2.legend(loc='upper left')
ax3.legend(loc='upper left')

#Create Chart Titles
ax1.set_title("Filament Diameter Plot")
ax2.set_title("Draw Speed Plot")
ax3.set_title("Feed Speed Plot")

#Create Chart X-Labels
ax1.set_xlabel("Time (s)")
ax2.set_xlabel("Time (s)")
ax3.set_xlabel("Time (s)")

#Create Chart Y-Labels
ax1.set_ylabel("Filament Diameter (mm)")
ax2.set_ylabel("Filament Draw Speed (m/min)")
ax3.set_ylabel("Preform Feed Speed (mm/min)")

#Adjust Y-Label Position
ax1.yaxis.set_label_position("right")
ax1.yaxis.tick_right()
ax2.yaxis.set_label_position("right")
ax2.yaxis.tick_right()
ax3.yaxis.set_label_position("right")
ax3.yaxis.tick_right()

#Add Plot Grids
ax1.grid()
ax2.grid()
ax3.grid()

#Loop Through Data
timeStart = time.time()
while True:
    try:
        #Read the Line
        s_bytes = serialCom.readline()
        decoded_bytes = s_bytes.decode("utf-8").strip('\r\n')

        #Parse the Line
        values = decoded_bytes.split(",")
        n = 0
        for n in range(len(values)):
            values[n] = float(values[n])
        print(values)

        #Append Values to Data Arrays
        timeVals.append(values[0])
        feedSpeedVals.append(values[1])
        drawSpeedVals.append(values[2])
        predictedDiamVals.append(values[3])
        measuredDiamVals.append(values[4])

        #Update Line Data
        line1.set_data(timeVals, predictedDiamVals)
        line2.set_data(timeVals, measuredDiamVals)
        line3.set_data(timeVals, drawSpeedVals)
        line4.set_data(timeVals, feedSpeedVals)

        #Automatically Update Axis 1 Limits
        ax1.relim()
        ax1.autoscale()

        #Automatically Update Axis 2 Limits
        ax2.relim()
        ax2.autoscale()

        #Automatically Update Axis 3 Limits
        ax3.relim()
        ax3.autoscale()

        #Updating Plot 1
        fig1.canvas.draw()
        fig1.canvas.flush_events()

        #Updating Plot 2
        fig2.canvas.draw()
        fig2.canvas.flush_events()

        #Updating Plot 3
        fig3.canvas.draw()
        fig3.canvas.flush_events()

    except:
        #Error for Bad Data
        print("ERROR: Line was not recorded!")
    
    #Check Timer
    timeCurrent = time.time()
    if timeInterval <= timeCurrent - timeStart:
        break