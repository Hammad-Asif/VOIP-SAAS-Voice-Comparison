from logging import exception
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
import datetime
import os.path
import time
from scipy.io import wavfile


def newest(path):
    files = os.listdir(path)
    paths = [os.path.join(path, basename)
             for basename in files if "wav" in basename]
    return max(paths, key=os.path.getctime)


def makeTime(start):
    start = int(start)
    seconds = (start/1000) % 60
    return str(datetime.timedelta(seconds=seconds))
    # seconds = int(seconds)
    # minutes = (start/(1000*60)) % 60
    # minutes = int(minutes)
    # hours = (start/(1000*60*60)) % 24
    # return str(hours)+":"+str(minutes)+":"+str(seconds)


def transcript(model, files):
    data = ""
    print("here")
    SetLogLevel(0)
    rec = KaldiRecognizer(model, 16000)
    endResult = []
    # wf, data = wavfile.read(file)
    output = open('output.json', 'r')
    output = json.load(output)
    output = output['segments']
    i = 0
    for file in files:
        wf = wave.open("segments/"+file, "rb")
        print("file read", i)
        txt = ""
        while True:
            data = wf.readframes(4000)
            try:
                if rec.AcceptWaveform(data):
                    temp = rec.Result()
                    # print(temp)
                    temp = eval(temp)
                    txt += temp["text"]
                if len(data) == 0:
                    txt = "Speaker"+str(output[i]["speaker"])+"\n" + makeTime(
                        output[i]["start"])+"--->"+makeTime(output[i]["end"])+"\n" + txt+"\n\n"

                    endResult.append(txt)
                    break
            except Exception as e:
                print("Error: ", e)
        wf.close()
        i += 1
    return endResult


def readFolder():
    files = os.listdir("segments")
    return files


if __name__ == '__main__':

    if not os.path.exists("model"):
        print("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        exit(1)

    # if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    #     print("Audio file must be WAV format mono PCM.")
    #     exit(1)

    # files=['43.wav','44.wav','45.wav','46.wav','47.wav','48.wav','49.wav','50.wav','51.wav','52.wav','53.wav']
    files = readFolder()
    model = Model("model")
    result = transcript(model, files)
    file = open("text.txt", "w")
    file.write(" ".join(result))
