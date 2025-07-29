import os
import time

def clearIt(delay=0):  
    if isinstance(delay, (int, float)) and delay > 0:
        time.sleep(delay)
    os.system('cls' if os.name == 'nt' else 'clear')