from flask import Flask, Response
from flask_cors import CORS
from flask_socketio import SocketIO
import controller as cont
import base64
from datetime import datetime
import subprocess
import os
import voskServer as vs
from vosk import Model, KaldiRecognizer, SetLogLevel
import threading

data=None
app = Flask(__name__)
cors = CORS(app)
socketio=SocketIO(app,cors_allowed_origins='*')
model = Model("model")
counter=0

def getTime():
    now = datetime.now()
    current_time = now.strftime("%H%M%S")
    return str(current_time)


def getAudio(encoded_string,file_name):
    encodedData=bytes(encoded_string, 'utf-8')
    decoded_audio = base64.decodebytes(encodedData) 
    audioFile = open(file_name, 'wb') 
    audioFile.write(decoded_audio)
    command = ['ffmpeg','-i',file_name,file_name[:-5]+'.wav']
    subprocess.run(command,stdout=subprocess.PIPE,stdin=subprocess.PIPE)
    return file_name[:-5]+'.wav'

@socketio.on('echo')
def echo(message):
    print(message)
    socketio.emit('echo', message)

@socketio.on("connect")
def connectServer():
    print("Client connected")
    socketio.send("connected","qweqwe")


@socketio.on("disconnect")
def disconnect():
    print('disconnected from server')


@socketio.on("streamdata")

def getData(data):
    
    global counter
    counter=counter+1
    streamData=data
    encodedData=""
    if(streamData):
        
        print('getting data from stream')
        # print("encoded data: ",data)
    
        socketio.emit('dataAuth', "data recieved by server")
        file_name=str(counter)+'.webm'
        file_name=getAudio(streamData, file_name)
        x = threading.Thread(target=vs.transcript, args=[model,file_name])
        x.start()

    else:
        print("failed to get data")


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)    


    
