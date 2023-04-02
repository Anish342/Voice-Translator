#add ease of selecting languages in combobox
#this is only english to other language work more on this!
#clean code and add comments
from tkinter import *
import textblob
from tkinter import ttk, messagebox
from playsound import playsound as PS
import speech_recognition as s_r
import googletrans
from gtts import gTTS
import os
import pyaudio
import pyttsx3


root = Tk()
root.title('Translator')
root.iconbitmap('C:\Voice Translator(needs work)')
root.geometry("880x300")

original_text = Text(root, height=10, width=40)
original_text.grid(row=0, column=0, pady=20, padx=10)


def record_1():
    r1 = s_r.Recognizer()
    with s_r.Microphone() as source:
    	r1.pause_threshold = 1
    	audio1 = r1.listen(source)

    try:
    	
		#original_text.insert(1.0,"Recognizing the voice...\n")
        query_1 = r1.recognize_google(audio1, language='en-in')
    	#original_text.insert(2.0,f"Recognized as : {query_1}\n")
        original_text.insert(1.0, query_1)
    except Exception as ep:
    	original_text.insert(1.0,"Sorry, it was not clear.Please repeat the sentence again...")
    	return "None"
    return query_1

rec=False
def record():
	query_1 = record_1()
	while(query_1 == 'None'):
    		query_1 = record_1()
	rec=True
	return query_1


words=''
x=''
to=''
def translate_it():
	# Delete Any Previous Translations
	translated_text.delete(1.0, END)

	try:
		# Get Languages From Dictionary Keys
		# Get the From Langauage Key
		for key, value in languages.items():
			if (value == original_combo.get()):
				from_language_key = key

		# Get the To Language Key
		for key, value in languages.items():
			if (value == translated_combo.get()):
				to_language_key = key

		if rec:
			words = textblob.TextBlob(record())
			print(words)
		else:
    			words = textblob.TextBlob(original_text.get(1.0, END))	
		# Turn Original Text into a TextBlob
		#original_text.insert(1.0,query_1)
		#words = textblob.TextBlob(query_1)

		# Translate Text		
		words = words.translate(from_lang=from_language_key , to=to_language_key)
		
		# Output translated text to screen
		translated_text.insert(1.0, words)
		x=str(words)
		speak = gTTS(text=x,lang=to_language_key, slow=False)
		if os.path.isfile('captured_JTP_voice.mp3'):
    			os.remove('captured_JTP_voice.mp3')
		# We will be using the save() function for saving the translated speech in #captured_JTP_voice.mp3 file
		speak.save("captured_JTP_voice.mp3")

		# Now at last, we will be using the OS module for running the translated voice.
		PS('captured_JTP_voice.mp3')		
		

	except Exception as e:
		messagebox.showerror("Translator", e)



def play():
	PS('captured_JTP_voice.mp3')
	#os.remove('captured_JTP_voice.mp3')		



def clear():
	# Clear the text boxes
	original_text.delete(1.0, END)
	translated_text.delete(1.0, END)

#language_list = (1,2,3,4,5,6,7,8,9,0,11,12,13,14,15,16,16,1,1,1,1,1,1,1,1,1,1,1,1,1)





# Grab Language List From GoogleTrans
languages = googletrans.LANGUAGES

# Convert to list
language_list = list(languages.values())




# Text Boxes


record_button = Button(root, text="Record", command=record)
record_button.grid(row=3,column=0,padx=5)
record_button.config( height =1, width = 5)

translate_button = Button(root, text="Translate!", font=("Helvetica", 24),command=translate_it)
translate_button.grid(row=0, column=1, padx=10, pady=10)

translated_text = Text(root, height=10, width=40)
translated_text.grid(row=0, column=2, pady=20, padx=10)
listen_button = Button(root, text="Play", command=play)
listen_button.grid(row=3,column=2,padx=5)
listen_button.config( height =1, width = 5)

# Combo boxes
original_combo = ttk.Combobox(root, width=50, value=language_list)
def search_o(event):
    value = event.widget.get()
    if value == '':
    	original_combo['value'] =language_list
    else:
        data=[]
        for item in language_list:
            if value.lower() in item.lower():
                data.append(item)
        original_combo['value'] = data


original_combo.set('Search')	
original_combo.bind('<KeyRelease>',search_o)
original_combo.current(21)
original_combo.grid(row=1, column=0)

translated_combo = ttk.Combobox(root, width=50, value=language_list)

def search(event):
    value = event.widget.get()
    if value == '':
    	translated_combo['value'] =language_list
    else:
        data=[]
        for item in language_list:
            if value.lower() in item.lower():
                data.append(item)
        translated_combo['value'] = data
    					

translated_combo.set('Search')	
translated_combo.bind('<KeyRelease>',search)
translated_combo.current(26)
translated_combo.grid(row=1, column=2)

# Clear button
clear_button = Button(root, text="Clear", command=clear)
clear_button.grid(row=2, column=1)

root.mainloop()
os.remove('captured_JTP_voice.mp3')
