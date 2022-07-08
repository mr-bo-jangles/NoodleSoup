from flask import Flask
from threading import Thread
from multiprocess import Process
import signal
import os

app = Flask('')

@app.route('/')
def home():
    return "Hello. I am alive!"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    process = Process(target=run)
    process.start()
    return process

def end_keep_alive(process):
  process.terminate()
  os.kill(1, signal.KILL)