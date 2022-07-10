from tkinter import Tk
from tkinter import Button
from pygame import mixer
from tkinter import filedialog
from tkinter import Label
import pyaudio
import wave
import struct

#My Project
my_song_vol=float(0.1)
#Now we define the window of our player
my_dy_player=Tk()
my_dy_player.title("Dushyant's Audio Player")

def play_in_delay():
    name_of_song_file = filedialog.askopenfilename(title="Select the song to play")
    playing_song = name_of_song_file
    lable_for_my_song = name_of_song_file.split("/")
    lable_for_my_song = lable_for_my_song[-1]
    print(lable_for_my_song)

    def clip16(x):
        # Clipping for 16 bits
        if x > 32767:
            x = 32767
        elif x < -32768:
            x = -32768
        else:
            x = x
        return (x)

    wavfile = name_of_song_file
    print('Play the wave file %s.' % wavfile)

    # Open the wave file
    wf = wave.open(wavfile, 'rb')

    # Read the wave file properties
    num_channels = wf.getnchannels()  # Number of channels
    RATE = wf.getframerate()  # Sampling rate (frames/second)
    signal_length = wf.getnframes()  # Signal length
    width = wf.getsampwidth()  # Number of bytes per sample

    print('The file has %d channel(s).' % num_channels)
    print('The frame rate is %d frames/second.' % RATE)
    print('The file has %d frames.' % signal_length)
    print('There are %d bytes per sample.' % width)

    # Set parameters of delay system
    b0 = 1.0  # Gain for direct path
    G = 0.8
    delay_sec = 0.1  # 100 milliseconds
    N = int(RATE * delay_sec)  # delay in samples

    print('The delay of %.3f seconds is %d samples.' % (delay_sec, N))

    # Create a buffer to store past values. Initialize to zero.
    BUFFER_LEN = N  # length of buffer
    buffer = BUFFER_LEN * [0]  # list of zeros

    # Open an output audio stream
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=RATE,
                    input=False,
                    output=True)

    # Get first frame (sample)
    input_bytes = wf.readframes(1)

    print('* Start')

    while len(input_bytes) > 0:
        # Convert binary data to number
        x0, = struct.unpack('h', input_bytes)

        # Compute output value
        # y(n) = b0 x(n) + G x(n-N)
        y0 = b0 * x0 + G * buffer[0]

        # Update buffer
        buffer.append(x0)
        del buffer[0]  # remove first value

        # Convert output value to binary data
        output_bytes = struct.pack('h', int(clip16(y0)))

        # Write output value to audio stream
        stream.write(output_bytes)

        # Get next frame (sample)
        input_bytes = wf.readframes(1)

    print('* Finished')

    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()

def play_lofi():
    name_of_song_file = filedialog.askopenfilename(title="Select the song to play")
    playing_song = name_of_song_file
    lable_for_my_song = name_of_song_file.split("/")
    lable_for_my_song = lable_for_my_song[-1]
    print(lable_for_my_song)

    def clip16(x):
        # Clipping for 16 bits
        if x > 32767:
            x = 32767
        elif x < -32768:
            x = -32768
        else:
            x = x
        return (x)

    wavefile = name_of_song_file

    print('Play the wave file %s.' % wavefile)

    # Open wave file (should be mono channel)
    wf = wave.open(wavefile, 'rb')

    # Read the wave file properties
    num_channels = wf.getnchannels()  # Number of channels
    RATE = wf.getframerate()  # Sampling rate (frames/second)
    signal_length = wf.getnframes()  # Signal length
    width = wf.getsampwidth()  # Number of bytes per sample

    print('The file has %d channel(s).' % num_channels)
    print('The frame rate is %d frames/second.' % RATE)
    print('The file has %d frames.' % signal_length)
    print('There are %d bytes per sample.' % width)

    # Difference equation coefficients
    b0 = 0.0004
    b2 = 0.0025
    b4 = 0.0004

    # a0 =  1.000000000000000
    a1 = -3.1806
    a2 = 3.8612
    a3 = -2.1122
    a4 = 0.4383

    # Initialization
    x1 = 0.0
    x2 = 0.0
    x3 = 0.0
    x4 = 0.0
    y1 = 0.0
    y2 = 0.0
    y3 = 0.0
    y4 = 0.0

    p = pyaudio.PyAudio()

    # Open audio stream
    stream = p.open(
        format=pyaudio.paInt16,
        channels=num_channels,
        rate=RATE,
        input=False,
        output=True)

    # Get first frame from wave file
    input_bytes = wf.readframes(1)

    while len(input_bytes) > 0:
        # Convert binary data to number
        input_tuple = struct.unpack('h', input_bytes)  # One-element tuple
        input_value = input_tuple[0]  # Number

        # Set input to difference equation
        x0 = input_value

        # Difference equation
        y0 = b0 * x0 + b2 * x2 + b4 * x4 - a1 * y1 - a2 * y2 - a3 * y3 - a4 * y4

        # y(n) = b0 x(n) + b2 x(n-2) + b4 x(n-4) - a1 y(n-1) - a2 y(n-2) - a3 y(n-3) - a4 y(n-4)

        # Delays
        x4 = x3
        x3 = x2
        x2 = x1
        x1 = x0
        y4 = y3
        y3 = y2
        y2 = y1
        y1 = y0

        # Compute output value
        output_value = int(clip16(y0))  # Integer in allowed range

        # Convert output value to binary data
        output_bytes = struct.pack('h', output_value)

        # Write binary data to audio stream
        stream.write(output_bytes)

        # Get next frame from wave file
        input_bytes = wf.readframes(1)

    print('* Finished')

    stream.stop_stream()
    stream.close()
    p.terminate()

def play_less_bass():
    name_of_song_file = filedialog.askopenfilename(title="Select the song to play")
    playing_song = name_of_song_file
    lable_for_my_song = name_of_song_file.split("/")
    lable_for_my_song = lable_for_my_song[-1]
    print(lable_for_my_song)

    def clip16(x):
        # Clipping for 16 bits
        if x > 32767:
            x = 32767
        elif x < -32768:
            x = -32768
        else:
            x = x
        return (x)

    wavefile = name_of_song_file

    print('Play the wave file %s.' % wavefile)

    # Open wave file (should be mono channel)
    wf = wave.open(wavefile, 'rb')

    # Read the wave file properties
    num_channels = wf.getnchannels()  # Number of channels
    RATE = wf.getframerate()  # Sampling rate (frames/second)
    signal_length = wf.getnframes()  # Signal length
    width = wf.getsampwidth()  # Number of bytes per sample

    print('The file has %d channel(s).' % num_channels)
    print('The frame rate is %d frames/second.' % RATE)
    print('The file has %d frames.' % signal_length)
    print('There are %d bytes per sample.' % width)

    # Difference equation coefficients
    # Difference equation coefficients
    b0 = 0.008442692929081
    b2 = -0.016885385858161
    b4 = 0.008442692929081

    # a0 =  1.000000000000000
    a1 = -3.580673542760982
    a2 = 4.942669993770672
    a3 = -3.114402101627517
    a4 = 0.757546944478829

    # Initialization
    x1 = 0.0
    x2 = 0.0
    x3 = 0.0
    x4 = 0.0
    y1 = 0.0
    y2 = 0.0
    y3 = 0.0
    y4 = 0.0

    p = pyaudio.PyAudio()

    # Open audio stream
    stream = p.open(
        format=pyaudio.paInt16,
        channels=num_channels,
        rate=RATE,
        input=False,
        output=True)

    # Get first frame from wave file
    input_bytes = wf.readframes(1)

    while len(input_bytes) > 0:
        # Convert binary data to number
        input_tuple = struct.unpack('h', input_bytes)  # One-element tuple
        input_value = input_tuple[0]  # Number

        # Set input to difference equation
        x0 = input_value

        # Difference equation
        y0 = b0 * x0 + b2 * x2 + b4 * x4 - a1 * y1 - a2 * y2 - a3 * y3 - a4 * y4

        # y(n) = b0 x(n) + b2 x(n-2) + b4 x(n-4) - a1 y(n-1) - a2 y(n-2) - a3 y(n-3) - a4 y(n-4)

        # Delays
        x4 = x3
        x3 = x2
        x2 = x1
        x1 = x0
        y4 = y3
        y3 = y2
        y2 = y1
        y1 = y0

        # Compute output value
        output_value = int(clip16(y0))  # Integer in allowed range

        # Convert output value to binary data
        output_bytes = struct.pack('h', output_value)

        # Write binary data to audio stream
        stream.write(output_bytes)

        # Get next frame from wave file
        input_bytes = wf.readframes(1)

    print('* Finished')

    stream.stop_stream()
    stream.close()
    p.terminate()

def pause_my_song():
    try:
        mixer.music.pause()
    except Exception as err2:
        print(err2)

def play_my_song():
    try:
        mixer.music.unpause()
    except Exception as err3:
        print(err3)

def desc_vol():
    try:
        global my_song_vol
        if my_song_vol<=0.1:
            my_label_for_vol.config(fg="Dark Blue",text="Minimum Volume reached")
            return
        my_song_vol=my_song_vol-float(0.1)
        mixer.music.set_volume(my_song_vol)
        my_label_for_vol.config(fg="Dark Blue", text="Current Volume:"+str((my_song_vol)))
    except Exception as err1:
        print(err1)


def inc_vol():
    try:
        global my_song_vol
        if my_song_vol>=1:
            my_label_for_vol.config(fg="Dark Blue",text="Maximum Volume Reached")
            return
        my_song_vol=my_song_vol+float(0.1)
        mixer.music.set_volume(my_song_vol)
        my_label_for_vol.config(fg="Dark Blue", text="Current Volume"+str(my_song_vol))
    except Exception as err1:
        print(err1)

#Here we are defining our functions
def listen_song():
    name_of_song_file = filedialog.askopenfilename(title="Select the song to play")
    playing_song=name_of_song_file
    lable_for_my_song=name_of_song_file.split("/")
    lable_for_my_song=lable_for_my_song[-1]
    print(lable_for_my_song)
    try:
        mixer.init()
        mixer.music.load(name_of_song_file)
        mixer.music.set_volume(my_song_vol)
        mixer.music.play()
        my_song_name_lable.config(fg="Dark Blue",text= "You are listening to:"+str(lable_for_my_song))
        my_label_for_vol.config(fg="Dark Blue", text="Volume:" + str(my_song_vol))
    except Exception as err :
        print(err)
        my_song_name_lable.config(fg="Dark Blue", text="Error occured")

#Now we will define a label for our window
Label(my_dy_player,text="Dushyant's Audio Player",font=("Monotype Corsiva",30),fg="Green").grid(sticky="N",row=2,padx=200)
Label(my_dy_player,text="Choose your favourite song",font=("Monotype Corsiva",20),fg="Dark Blue").grid(sticky="N",row=4,padx=200)
Label(my_dy_player,text="Volume Level",font=("Monotype Corsiva",20),fg="Dark Blue").grid(sticky="w",row=8,padx=0)
my_song_name_lable=Label(my_dy_player,font=("Times",20))
my_song_name_lable.grid(stick="N",row=6)
my_label_for_vol=Label(my_dy_player,font=("Times",20))
my_label_for_vol.grid(stick="N",row=8)

#Now we will place the button which are required
Button(my_dy_player,text="Choose the song",font=("Times",15),command=listen_song).grid(row=5,sticky="N")
Button(my_dy_player,text="Play the Song",font=("Times",15),command=play_my_song).grid(row=6,sticky="E")
Button(my_dy_player,text="Increase the Volume",font=("Times",15),command=inc_vol).grid(row=6,sticky="w")
Button(my_dy_player,text="Decrease the Volume",font=("Times",15),command=desc_vol).grid(row=10,sticky="w")
Button(my_dy_player,text="Pause the song",font=("Times",15),command=pause_my_song).grid(row=10,sticky="e")
Button(my_dy_player,text="Play song in Lo-fi",font=("Times",15),command=play_lofi).grid(row=12,sticky="e")
Button(my_dy_player,text="Play song with Less Bass",font=("Times",15),command=play_less_bass).grid(row=14,sticky="e")
Button(my_dy_player,text="Play song with Delay",font=("Times",15),command=play_in_delay).grid(row=16,sticky="e")
my_dy_player.mainloop()