from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import speech_recognition as sr
import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Tk 
from tkinter.filedialog import askopenfilename

s=''

def where_it_all_happens():
    audio_segment = AudioSegment.from_mp3(s)
    normalized_sound = match_target_amplitude(audio_segment, -20.0)

    #Print detected non-silent chunks, which in our case would be spoken words.
    nonsilent_data = detect_nonsilent(normalized_sound, min_silence_len=int(milimin_value.get()), silence_thresh=-50, seek_step=1)

    i = 0

    print('Making Directory...')

    try:
        os.mkdir(str('final'))
    except(FileExistsError):
        pass

    print('Directory made!')

    os.chdir(str('final'))

    for chunks in nonsilent_data:

        print('On file number ' + str(i))

        audio_chunk = audio_segment[chunks[0]-300:chunks[1]+300]

        audio_chunk.export("./{0}chunk.wav".format(i), bitrate ='192k', format ="wav")

        filename = './' + str(i)+'chunk'+'.wav'

        file = filename

        r = sr.Recognizer()

            # recognize the chunk
        with sr.AudioFile(file) as source:
            r.adjust_for_ambient_noise(source)
            audio_listened = r.listen(source)

        try:
            # try converting it to text
            rec = r.recognize_google(audio_listened)
            new_name = "./" + str(i) + rec + ".wav"
            try:
                os.rename(filename, new_name)
            except FileExistsError:
                
                os.remove(new_name)
                os.rename(filename, new_name)
            except OSError:
                print('error!')

        # catch any errors.
        except sr.UnknownValueError:
            print("Could not understand audio")

        except sr.RequestError as e:
            print("Could not request results. check your internet connection")

    

        i += 1
    window.destroy()

def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

def append_file_name():
    global s
    s = askopenfilename()
    selected_file.config(text=s)

window = tk.Tk()

title = ttk.Label(text='Welcome to this audio splicer!')
milimin_prompt = ttk.Label(text='What is the minimum amount of time that must pass between words for it to count as the end of a sentence? (written in miliseconds, 700 works pretty well)')
milimin_value = ttk.Entry()
request_file = ttk.Button(text='Click to select file to splice',command=append_file_name)
finish = ttk.Button(text='If everything is correct, press this button to splice!', command=where_it_all_happens)
selected_file = ttk.Label(text="(No file selected)")

title.pack()
request_file.pack()
selected_file.pack()
milimin_prompt.pack()
milimin_value.pack()
finish.pack()
window.mainloop()
files = []

""""
filenum = input('How many files do you want to split?')

minlength = input('What is the minimum amount of time that must pass between words for it to count as the end of a sentence? (written in miliseconds, 700 works pretty well)')

for i in range(int(filenum)):
    files.append(askopenfilename())

print(files)

#adjust target amplitude
def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

#Convert wav to audio_segment
audio_segments = []
for f in files:
    audio_segments.append(AudioSegment.from_mp3(f))

j = 0

for audio_segment in audio_segments:
    normalized_sound = match_target_amplitude(audio_segment, -20.0)
    print("length of audio_segment={} seconds".format(len(normalized_sound)/1000))

    #Print detected non-silent chunks, which in our case would be spoken words.
    nonsilent_data = detect_nonsilent(normalized_sound, min_silence_len=int(minlength), silence_thresh=-50, seek_step=1)

    #convert ms to seconds
    print("start,Stop")
    for chunks in nonsilent_data:
        print(chunks)

    i = 0

    try:
        os.mkdir(str(j))
    except(FileExistsError):
        pass

    os.chdir(str(j))

    for chunks in nonsilent_data:

        audio_chunk = audio_segment[chunks[0]-300:chunks[1]+300]

        audio_chunk.export("./{0}chunk.wav".format(i), bitrate ='192k', format ="wav")

        filename = './' + str(i)+'chunk'+'.wav'

        file = filename

        r = sr.Recognizer()

            # recognize the chunk
        with sr.AudioFile(file) as source:
            r.adjust_for_ambient_noise(source)
            audio_listened = r.listen(source)

        try:
            # try converting it to text
            rec = r.recognize_google(audio_listened)
            new_name = "./" + str(i) + rec + ".wav"
            try:
                os.rename(filename, new_name)
            except FileExistsError:
                os.remove(new_name)
                os.rename(filename, new_name)
            except OSError:
                print('error!')

        # catch any errors.
        except sr.UnknownValueError:
            print("Could not understand audio")

        except sr.RequestError as e:
            print("Could not request results. check your internet connection")

    

        i += 1
    j += 1

"""