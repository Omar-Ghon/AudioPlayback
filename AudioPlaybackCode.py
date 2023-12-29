import time
import wave
import pyaudio
import Gamepad

#Gamepad library settings and checking it's connected
gamepadType = Gamepad.Arcade
if not Gamepad.available():
    print("Connect Gamepad")
    while not Gamepad.available():
        time.sleep(1.0)
print("Gamepad connected!")


#Defining global variables
button1 = '1'
button2 = '2'
button3 = '3'
button4 = '4'
button5 = '5'
button6 = '6'
button7 = '7'
button8 = '8'
button9 = '9'
pollInterval = 0.1

#Defining and starting Gamepad
gamepad = gamepadType();
gamepad.startBackgroundUpdates()

def button():
    pressed_bool = True
    while pressed_bool:
        for i in range(1, 10):
            if gamepad.beenReleased(str(i)):
                pressed_bool = False
                print("Button ", i, " was pressed")
                return (int (i))
            
def play_audio(filename):
    #setup and open file

    chunk = 1024
    wf = wave.open((str(filename)+".wav"), 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(), 
                    rate = wf.getframerate(),
                    output = True)
    data = wf.readframes(chunk)

    #play audio of data
    while data:
        stream.write(data)
        data = wf.readframes(chunk)
    
    #clean-up
    wf.close()
    stream.close()
    p.terminate()

def record_audio(filename):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 5 #record for 5 seconds
    output_file = (str(filename) + ".wav")

    with wave.open(output_file, 'wb') as wf:
        p = pyaudio.PyAudio()
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(CHUNK))
        wf.setframerate(RATE)

        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)
        print("Recording...")
        for _ in range(0, RATE//CHUNK*RECORD_SECONDS):
            wf.writeframes(stream.read(CHUNK))
        print('Done')

    stream.close()
    p.terminate()

def choose_num():
    print("Choose number 1-9")

def main():
    chosen_button = button()

    if chosen_button <= 6: #6 storage buttons play audio when pressed
        file = "Audio_File_" + str(chosen_button)
        try:
            play_audio(file)
        except:
            choose_num()
    
    elif chosen_button >= 7:
        time.sleep(0.1)
        num = button()
        if num <= 6:
            file = "Audio_File_" + str(num)
            record_audio(file)
    else:
        choose_num()

while True: #run main forever
    main()

gamepad.disconnect() #to disconnect when done