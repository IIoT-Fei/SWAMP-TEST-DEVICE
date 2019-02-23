import sys
import Adafruit_DHT
import requests
import json

url = 'http://192.168.0.4:7896/iot/json?i=Probe111&k=key123'

headers = {
	'content-type': 'application/json',
	'fiware-service':'iot_lab',
	'fiware-servicepath':'/'
}

# Parse command line parameters.
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }
if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
    sensor = sensor_args[sys.argv[1]]
    pin = sys.argv[2]
else:
    print('Usage: sudo ./Adafruit_DHT.py [11|22|2302] <GPIO pin number>')
    print('Example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO pin #4')
    sys.exit(1)

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)


payload = {
	'temperature':temperature,
	'humidity':humidity
}

r = requests.post(url, data=json.dumps(payload), headers=headers)


# Un-comment the line below to convert the temperature to Fahrenheit.
# temperature = temperature * 9/5.0 + 32

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%  status_code={2}'.format(temperature, humidity, r.status_code))
else:
    print('Failed to get reading. Try again!')
    sys.exit(1)

