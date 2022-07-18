import time
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter.ttk import Progressbar
import numpy as np
import trimesh
import os
from tkinter import messagebox
from PIL import Image, ImageTk



root=Tk()
root.title("STL Maker")
root.geometry("450x550")
root.resizable(False,False)
root.config(bg='#f4fdfe')#82ccdd
photo=PhotoImage(file='images/stllogo.png')
root.iconphoto(False,photo)


Label1=Label(root, text="Convert STEP, IGS ,BREP ,Nastran ,Abaqus 3D Model into STL Model", font="New 10 bold", bg="#f4fdfe")
Label1.grid(row=1, column=0,pady=20)
label2=Label(root, text='Browse 3D Model',font="Ariel 10 bold",bg='#f4fdfe')
label2.grid(row=4,column=0)
label2=Label(root, text='Convert To STL',font="Ariel 10 bold",bg='#f4fdfe')
label2.grid(row=7,column=0)
Browse_entry=Entry(root,font="Ariel 15 bold",bg='white')
Browse_entry.grid(row=2,column=0,columnspan=3, pady=10)

def loadfile():
    
    global openfile
    
    openfile=filedialog.askopenfilename(initialdir="os.getcwd()",title="Please Select Model", filetypes=[("IGS",".igs"),("STEP",".STEP"),("BREP",".brep"),("Nastran",".bdf"),("Gmsh",".msh"),("Abaqus",".inp"),("Diffpack ",".diff"),("Inria Medit",".mesh"),("All Files","*.*")])
    
    if openfile:
        global Browse_entry
        try:
            Browse_entry.insert(0,openfile)
            messagebox.showinfo("Imported","File is imported Successfully, Now Click on Convert")    
        except:
            messagebox.showinfo('Select 3D Model','3D Model is not selected')
    else:
        Browse_entry.delete(0,END)
def convert():    
    global openfile
    global mesh
    global exportfile
    
    exportfile=filedialog.asksaveasfile(initialdir="os.getcwd()",defaultextension=".stl", title="Save As")
    
    if exportfile:
        try:    
            global Browse_entry
            for i in range(5):
                root.update_idletasks()
                Progressbar1['value'] += 20
                time.sleep(1)
            mesh = trimesh.Trimesh(**trimesh.interfaces.gmsh.load_gmsh(file_name=openfile, gmsh_args = [
                ("Mesh.Algorithm", 1), #Different algorithm types, check them out
                ("Mesh.CharacteristicLengthFromCurvature", 50), #Tuning the smoothness, + smothness = + time
                ("General.NumThreads", 20), #Multithreading capability
                ("Mesh.MinimumCirclePoints", 74)])) 
            mesh.export(exportfile.name)
            messagebox.showinfo("Success","File is Successfully Converted and Saved into\n"+str(exportfile.name))
            Browse_entry.delete(0,END)
            Progressbar1.stop()     
        except:
            messagebox.showinfo('Alert','unexpected things happened Please follow the sequence')
            Progressbar1.stop()    
def quit():
    root.quit()

def help():
    messagebox.showinfo('help','Step(1) Browse, Step(2) Convert and Enjoy')

def thanks():
    messagebox.showinfo('Thanks',"This Version v1.0 of This Tool is Under Construction Thanks For Using STL Maker")
    

Progressbar1=ttk.Progressbar(root,orient=HORIZONTAL,length=300,mode="determinate")
Progressbar1.grid(row=8,column=0,pady=20)


img1= (Image.open("images/browse.png"))
resized_image1= img1.resize((120,100))
new_image1= ImageTk.PhotoImage(resized_image1)

img2= (Image.open("images/convert.png"))
resized_image2= img2.resize((120,100))
new_image2= ImageTk.PhotoImage(resized_image2)

filebrowse=Button(root,image=new_image1,command=loadfile,font="Ariel 10 bold", pady=10)
filebrowse.grid(row=3, column=0, pady=10)
fileconvert=Button(root, image=new_image2, command=convert,font="Ariel 10 bold",pady=10)
fileconvert.grid(row=6, column=0, pady=10)
fileexit=Button(root, text="Close", command=quit ,font="Ariel 10 bold", padx=38, pady=10)
fileexit.grid(row=9, column=0, pady=10)

submenu=Menu(root)
m1=Menu(submenu,tearoff=0)
m1.add_command(label='Browse',command=loadfile)
m1.add_command(label='Convert',command=convert)
m1.add_command(label='Exit',command=quit)
root.config(menu=submenu)
submenu.add_cascade(label='File',menu=m1)
submenu.add_cascade(label='Help',command=help)
submenu.add_cascade(label='About',command=thanks)



root.mainloop()
