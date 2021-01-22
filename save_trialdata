from __future__ import print_function


import atexit
from os import path
from json import dumps, loads
import cardata

#create file counter
def read_counter():
    return loads(open("counter.json", "r").read()) + 1 if path.exists("counter.json") else 0


def write_counter():
    with open("counter.json", "w") as f:
        f.write(dumps(counter))


counter = read_counter()
atexit.register(write_counter)
df = cardata.main()
df.to_csv(r'/home/pi/Desktop/csvFile/file{}data.csv'.format(counter), index = False) #saves data from cardata as csv
