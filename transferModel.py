from vosk import Model, KaldiRecognizer, SetLogLevel
import os


if __name__ == '__main__':

    if not os.path.exists("model"):
        print("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        exit(1)

        # if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        #     print("Audio file must be WAV format mono PCM.")
        #     exit(1)

    # files=['43.wav','44.wav','45.wav','46.wav','47.wav','48.wav','49.wav','50.wav','51.wav','52.wav','53.wav']
    model = Model("model")
    print(type(model))
    print(model)
