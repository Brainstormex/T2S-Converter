
import tkinter as tk					
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import showinfo, showwarning
import pyttsx3
import win32api
from tkinter import filedialog
import speech_recognition as sr
from PIL import ImageTk, Image 

#from ttkthemes import ThemedTk,THEMES

window = tk.Tk()


style = ttk.Style()
 
style.theme_create('pastel', settings={
    ".": {
        "configure": {
            "background": '#ccffff', # All except tabs
            "font": 'red'
        }
    },
    "TNotebook": {
        "configure": {
            "background":'#848a98', # Your margin color
            "tabmargins": [2, 5, 0, 0], # margins: left, top, right, separator
        }
    },
    "TNotebook.Tab": {
        "configure": {
            "background": '#ccffcc', # tab color when not selected
            "padding": [10, 2], # [space between text and horizontal tab-button border, space between text and vertical tab_button border]
            "font":"white"
        },
        "map": {
            "background": [("selected", '#ccffff')], # Tab color when selected
            "expand": [("selected", [1, 1, 1, 0])] # text margins
        }
    }
})


#style = ttk.Style()
window.title("T2S & S2T")

tabControl = ttk.Notebook(window)
tabControl.grid_rowconfigure([0], weight=1)
style.theme_use('pastel')
#style.configure("TNotebook", background='#ccffcc')
style.configure("TNotebook.Tab", fg='red')
#style.configure("TFrame", background='blue')
style.configure("TNotebook", tabposition='n')
window.grid_columnconfigure([0, 1,2], weight=1)
window.grid_rowconfigure([0,1], weight=1)
window.config(bg='#848a98')

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
app_height=500
app_width=600
x = (screen_width/2)-(app_width/2)
y = (screen_height/2)-(app_height/2)
window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

tabControl.add(tab1, text ='Text To Speech')
tabControl.add(tab2, text ='Speech To Text')
tabControl.grid(row=0, column=0, columnspan=3,padx=15,pady=5, sticky="ewns")

photo = ImageTk.PhotoImage(image=Image.open('icon.png'))
window.iconphoto(False, photo)

tab1f = tk.LabelFrame(tab1,text='Text Box',font=('lucida 20 bold italic', 10),padx=5,pady=5)
tab1f.grid(row=0,column=0,columnspan=3,padx=10,pady=30, sticky="ewns")

tab2f = tk.LabelFrame(tab2,text='Text Box',font=('lucida 20 bold italic', 10),padx=5,pady=5)
tab2f.grid(row=0,column=0,columnspan=3,padx=10,pady=30, sticky="ewns")

tab1f.grid_columnconfigure([0,1,2], weight=1)
tab1f.grid_rowconfigure([0,1], weight=1)
tab2f.grid_columnconfigure([0,1,2], weight=1)
tab2f.grid_rowconfigure([0,1], weight=1)

# all of my function
# text to speech functions
def play():
    engine = pyttsx3.init()
    engine.setProperty('rate',125)
    voices=engine.getProperty('voices')
    engine.setProperty('voice',voices[1].id)
    audio_string = text2.get('0.0',tk.END)

    engine.say(audio_string)
    engine.runAndWait()
    engine.stop()
    if text2.compare("end-1c", "==", "1.0"):
        showwarning('Text To Speech','Text Box is Empty')

def save():
    if text2.compare("end-1c", "==", "1.0"):

        showwarning('Text To Speech','Text Box is empty')
    else:
        engine = pyttsx3.init()
        audio_string = text2.get('0.0',tk.END)
#        save_sound = filedialog.asksaveasfile(defaultextension=' .wav', filetypes=[("WAV file",".wav"),
#                                                                                    ("MP3 file",".mp3"),
#                                                                                    ("M4A file",".m4a")])
        engine.save_to_file(audio_string, 'sound.wav' )
        engine.runAndWait()
        engine.stop()
        showinfo('Text To Speech','Your file is saved')
    

#def my_popup(e):
#    my_menu.tk_popup(e.x_root,e.y_root)

def dialog():    
    if text3.compare("end-1c", "==", "1.0"):
    
        showwarning('Speech To Text','Text Box is Empty')
    else:
    
        file = filedialog.asksaveasfile(defaultextension=' .txt', filetypes=[("Text file",".txt"),
                                                                            ("HTML file",".html"),
                                                                            ("PDF file",".pdf")])
        
        
        filetext = str(text2.get(0.0,tk.END))
        file.write(filetext)
        file.close
    

def open_text():
    try:
        file = filedialog.askopenfilename(filetypes=[("Text file",".txt"),
                                                    ("PDF file",".pdf"),
                                                    ("DOCX file",".docx"),
                                                    ("DOC file",".doc")])

    
        content = open(file).read()
        text2.insert(tk.END, content)
        print(content)
    except FileNotFoundError:
        showinfo('Text To Speech','File not Selected')

#speech to text function
recog = sr.Recognizer()
#print(sr.Microphone.list_microphone_names())
#text =''
def speak():

#    global text
    with sr.Microphone() as source:
        recog.adjust_for_ambient_noise(source, duration=1)
        print('Speak : ')
        audio_data = recog.listen(source)

#       global text
        try:

            text = recog.recognize_google(audio_data)
            print('You Said : {}'.format(text))
            text3.insert(tk.END, ''+text)
#        except OSError as e:
#            showinfo('Speech To Text','No Input Device Available')

        except:
            showinfo('Speech To Text','Error while recording your voice')

def openfile():
    try:
        open_sound = filedialog.askopenfilename(filetypes=[("wav file",".wav")])
        with sr.AudioFile(open_sound) as file:
            audio_data = recog.record(file)
            text = recog.recognize_google(audio_data)
            print('Audio has {}'.format(text))
            text3.insert(tk.END, ''+text)        
    except FileNotFoundError:
        showinfo('Speech To Text','No Audio file selected')
    except sr.UnknownValueError:
        showwarning('Speech To Text','Cannot Retrive Audio from the selected file')

tab1.grid_columnconfigure([0,1,2], weight=1)
tab1.grid_rowconfigure([0,1], weight=1)

text2 = ScrolledText(tab1f,wrap=tk.WORD,padx=10,pady=10,relief=tk.RIDGE)
text2.grid(row=1,column=0,columnspan=3,sticky="ewns")

text3 = ScrolledText(tab2f,wrap=tk.WORD,padx=10,pady=10,relief=tk.RIDGE)
text3.grid(row=1,column=0,columnspan=3,sticky="ewns")
#speak()
#text3.insert(tk.END, 'Fact'+text)

tab2.grid_columnconfigure([0,1,2], weight=1)
tab2.grid_rowconfigure([0,1], weight=1)

im1 = Image.open('playbutton2.jpg')
im2 = Image.open('opentext1.jpg')
im3 = Image.open('saveaudio1.jpg')
im4 =Image.open('speakbutton1.jpg')
im5 =Image.open('openaudio2.jpg')
im6 =Image.open('savetext1.jpg')
photo1 = ImageTk.PhotoImage(image=im1)
photo2 = ImageTk.PhotoImage(image=im2)
photo3 = ImageTk.PhotoImage(image=im3)
photo4 = ImageTk.PhotoImage(image=im4)
photo5 = ImageTk.PhotoImage(image=im5)
photo6 = ImageTk.PhotoImage(image=im6)


tk.Button(tab1,text='Play',image=photo1,command=play, borderwidth=0).grid(row=2,column=0,padx=2,pady=10)
tk.Button(tab1,text='Open txt', image=photo2, command=open_text, borderwidth=0).grid(row=2,column=1,ipadx=2,pady=10)
tk.Button(tab1,text='Save Audio', image=photo3, command=save, borderwidth=0).grid(row=2,column=2,padx=2,pady=10)

tk.Button(tab2,text='Speak',image=photo4,command=speak, borderwidth=0).grid(row=2,column=0,padx=2,pady=10)
tk.Button(tab2,text='Open Audio',image=photo5,command=openfile, borderwidth=0).grid(row=2,column=1,padx=2,pady=10)
tk.Button(tab2,text='Save text',image=photo6,command=dialog, borderwidth=0).grid(row=2,column=2,padx=2,pady=10)

#lambda : text3.delete('0.0',tk.END)).grid(row=2,column=1,padx=2)
#my_menu = tk.Menu(window, tearoff=False, bg='white')
#my_menu.add_command(label='save as text',command=dialog)
#my_menu.add_command(label='male voice')
#my_menu.add_command(label='female voice')
#window.bind("<Button - 3>", my_popup)


window.mainloop()   
