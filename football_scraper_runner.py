from multiprocessing import Process
import sys, time
from api.contact import addFootballDataToServer

print(f"Football League Runner Started..")
sys.stdout.flush()

def job():
    addFootballDataToServer()

while True:
    job()
    time.sleep(600)
