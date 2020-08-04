import tkinter as tk
from tkinter import filedialog , Text
import os 
import requests
from tkinter import messagebox
import time
import concurrent.futures


root = tk.Tk()
folderPath = None
images = []

def insert_image():
    url = textbox.get('1.0','end-1c')
    textbox.delete(1.0,tk.END)
    try: 
        r = requests.get(url)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        messagebox.showerror(title='Invalid url', message='An invalid url has been inserted.\nPlease insert a valid url.')
    else:
        images.append(url)
        frame_append_image()

def frame_append_image():
    for widget in frame.winfo_children():
        widget.destroy()

    for image in images:
        label = tk.Label(frame, text=image , bg='#eee')
        label.pack()

def downloadImages():
    if not len(images):
        messagebox.showwarning('Warning' , 'Not inserted any images.')
    else:
        global folderPath
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(download_image,images)
        messagebox.showinfo('Images info',f'Images downloaded successfully , you can see them in:\n {folderPath}')
        
def download_image(url):
        img_bytes = requests.get(url).content
        image_name = url.split('/')[3]
        img_name = f'{image_name}.jpg'
        path = f'{folderPath}/{img_name}' if folderPath  else img_name
        with open(path,'wb') as img_file:
            img_file.write(img_bytes)
            print(f'{img_name} was downloaded....')

def selectPath():
     global folderPath
     folderPath = filedialog.askdirectory()
     print(folderPath)

textbox = tk.Text(root, height=1, width=40 )
textbox.insert(tk.END, "Insert an image url...")
textbox.pack()

insertImage = tk.Button(root,text='Insert Image',height=1 , width=17 , padx=100,pady=2,fg='white',bg='#263d42' , command=insert_image)
insertImage.pack()

canvas = tk.Canvas(root, height=600, width=700 , bg='#263d42')
canvas.pack()

frame = tk.Frame(root , bg='white')
frame.place(relwidth=0.8,relheight=0.7,relx=0.1,rely=0.1)

downloadBtn = tk.Button(root,text='Download Images',padx=100,pady=5,fg='white',bg='#263d42',height=2 , width=30,command=downloadImages)
downloadBtn.pack()

folderPicker = tk.Button(root,text='Select storage location' ,padx=100,pady=2,fg='white',bg='#263d42', height=2 , width=30 , command=selectPath)
folderPicker.pack(pady=10)

root.resizable(0,0)
root.mainloop()