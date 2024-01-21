from vosk import Model, KaldiRecognizer, SetLogLevel
import os
import wave
import socket
import threading
import time
import json
import string
import random
import jsonify
from shutil import copyfile

HEADER = 20
SLICE_SIZE = 4096
PORT = 5050
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def transcript(model,file):
    data=""
    
    
    next_file=str(int(file.split('.')[0])+1)+'.'+'wav'
    SetLogLevel(0)
    wf = wave.open(file, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    endResult = []
    print("file read")
    while True:
        
        data = wf.readframes(4000)
        
        if rec.AcceptWaveform(data):
            temp = rec.Result()
            print(temp)
            temp = eval(temp)
            # endResult.append(temp["text"])
        if len(data) == 0:
            
            while not os.path.exists(next_file):
                print("waiting for next file")
                time.sleep(1)

            if os.path.isfile(next_file):
                wf = wave.open(next_file, "rb")
                next_file=str(int(next_file.split('.')[0])+1)+'.'+'wav'
                print('nextloop=============================>>>>>>>>>>>>>>>>>>>>',next_file)
                
            
            
    wf.close()