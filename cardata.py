from __future__ import print_function


import atexit
from os import path
from json import dumps, loads

import numpy as np
import pandas as pd
import cv2
import car

######################################################################################################################################################
#create file counter
def read_counter():
    return loads(open("counter.json", "r").read()) + 1 if path.exists("counter.json") else 0


def write_counter():
    with open("counter.json", "w") as f:
        f.write(dumps(counter))


counter = read_counter()
atexit.register(write_counter)
######################################################################################################################################################



def main():
    df = pd.DataFrame(columns = ['filename','trial','lognum', 'left', 'right', 'straight', 'forward', 'backward', 'stopped'])
    logger = car.main(counter) #get data from car

    for i in range(len(logger)):
        value = logger[i].values()
        items_list = list(value)
        df.loc[i] = items_list # add data to dataframe
        i+=1
    print(df)
    return df


