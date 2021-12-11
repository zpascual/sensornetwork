import sys
import Adafruit_BBIO.GPIO as BBGPIO
import numpy as np
import pandas as pd
import constants
import ports

def main():
    #init sensors
    initSensor(8, ports.masterTempSensor)
    initSensor(8, ports.slaveTempSensor)
    initSensor(8, ports.masterPressureSensor)
    initSensor(8, ports.altPressureSensor)
    initSensor(8, ports.linearPot)
    
    #check sensors
    checkSensor(8, ports.masterTempSensor)
    checkSensor(8, ports.slaveTempSensor)
    checkSensor(8, ports.masterPressureSensor)
    checkSensor(8, ports.altPressureSensor)
    checkSensor(8, ports.linearPot)
    
    data = pd.read_csv(r'50KResistorTable.csv')
    df = pd.DataFrame(data, columns= ['F','Ohms'])
    
    degF, resistance = df(1), df(2)
    
    return None

def initSensor(bank, sensorPort):
    if bank == 8:
        BBGPIO.setup("P8_"+str(sensorPort), BBGPIO.IN)
    else:
        BBGPIO.setup("P9_"+str(sensorPort), BBGPIO.IN)
        
def readSensor(bank, sensorPort):
    if bank == 8:
        BBGPIO.input("P8_"+str(sensorPort))
    else:
        BBGPIO.input("P9_"+str(sensorPort))
    
def checkSensor(bank, sensorPort):
    if readSensor(bank, sensorPort) <= constants.pressureMinVolt:
        print("Issue with sensor at port %f. Sensor reading below min spec value.", sensorPort)
        exit

def convertVoltageToPressure(volts):
    pressure = (volts-constants.pressureMinVolt)/(constants.pressureMaxVolt-constants.pressureMinVolt)
    return pressure

if __name__ == "__main__":
    main()