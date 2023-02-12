import time
import board
import adafruit_bno055
import ms5837

class Sensors:
    def tempSensor():
        i2c = board.I2C()  # uses board.SCL and board.SDA
        # i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
        try: sensor = adafruit_bno055.BNO055_I2C(i2c)
        except: print("Cannot connect to the bno055 sensor (Temp Fail)")
        else:

            global last_val
            last_val = 0xffff

            result = sensor.temperature()
            if abs(result - last_val) == 128:
                result = sensor.temperature
                if abs(result - last_val) == 128:
                    return 0b00111111 & result
            last_val = result
            return result

    def orientationSensor():
        i2c = board.I2C()

        try: sensor = adafruit_bno055.BNO055_I2C(i2c)
        except: print ("Cannot connect to the bno055 sensor (Orientation Fail)")
        else:
            quaternion = tuple()
            quaternion = sensor.quaternion()
            return quaternion

    def pressureSenor():
        sensor = ms5837.MS5837()
        try: sensor.init()
        except: print("Cannot connect to the pressure sensor")
        else:
            sensor.setFluidDensity(ms5837.DENSITY_FRESHWATER)
            return sensor.read()

while 1:
    tempSensor = Sensors.tempSensor()
    orientationSensor = Sensors.orientationSensor()
    pressureSenor = Sensors.pressureSenor()

    print(f"Temp value: {tempSensor}, Orientation value: {orientationSensor}, Sensor value: {pressureSenor}")

    time.sleep(0.1)