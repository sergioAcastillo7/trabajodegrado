import serial
import time
import tkinter
import tkinter as tk
from tkinter import * 
from tkinter import messagebox
from tkinter import filedialog
import pymysql
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pyplot 
import matplotlib.animation as animation
from datetime import datetime
import os
from PIL import Image, ImageTk
from tkinter import messagebox, PhotoImage
import cv2
import imutils


def menu_pantalla():
    
    global pantalla
    pantalla=tk.Tk()
    pantalla.geometry("600x600+100+100")
    pantalla.config(bg="white")
    pantalla.title("Bienvenidos")
    
    titulo = Label(pantalla, text="UNIVERSIDAD DE PAMPLONA",bg="white").pack()
    titulo = Label(pantalla, text="Arquitectura para monitoreo de variables físicas",bg="white").pack()
    titulo = Label(pantalla, text="Sergio Castillo",bg="white").pack()
    Label(pantalla, text="")
    image=PhotoImage(file="logo.gif")
    image=image.subsample(2,2)
    label=Label(image=image).place(x=2, y=3)
    
    
    image2=PhotoImage(file="ing.gif")
    image2=image2.subsample(4,4)
    label=Label(image=image2).place(x=480, y=3)
  
   
    l3=Label(pantalla, text="ACCESO AL SISTEMA",bg="white").place(x=240,y=200)
  
    Button(text="Datos tiempo real", height="3", width="30", bg="white",comman=sensores).place(x=170,y=250)
   

    Button(text="Iniciar Sesión", height="3", width="30",bg="white", comman=inicio_sesion).place(x=170,y=350)
    
    
    Button(text="Ayuda", height="3", width="30",bg="white", comman=render).place(x=170,y=450)


    pantalla.mainloop()


def sensores():
    
    global pantalla1, guard
    pantalla1 = Toplevel(pantalla)
    pantalla1.geometry("300x300")
    pantalla1.config(bg="white")
    pantalla1.title("Variables a mostras")
    Label(pantalla1, text="Sensores",bg="white").pack()
    Label(pantalla1, text="",bg="white").pack()
    
    Button(pantalla1, text="Lluvia", height="3", width="30",bg="white", command=puerto_serial_lluvia).pack()
    Label(text="").pack()
     
    Button(pantalla1, text="Temperatura/Humedad", height="3",bg="white", width="30", command=puerto_serial_H_T).pack()
    Label(text="").pack()
    
    
def puerto_serial_lluvia():
    

    ser = serial.Serial('/dev/ttyACM0',9600)
    ser.flushInput()
    fig = plt.figure()
    ax=fig.add_subplot(1,1,1)
    xdatos, ydatos = [], []
    ax.grid(True)
    ax.set_title("Lluvia")

    now = datetime.now()
    fecha =now.strftime('%d.%m.%Y')
    nombre = '/home/pi/Desktop/Proyecto/Historial Datos/lluvia_' + fecha + '.txt'
    
    while True:
      
        try:
            
            lineBytes = ser.readline()
            line = lineBytes.decode('utf-8')
            
            
            def animate(i,xdatos,ydatos):
                
                datos = ser.readline()
                line = datos.decode('utf-8')
                v_lluvia = line.split(",")[0]
                datos = float(v_lluvia)
                xdatos.append(i)
                ydatos.append(datos)
                np.savetxt(nombre,ydatos)
                
                ax.plot(xdatos,ydatos)
                ax.set_xlabel('Segundos')
                ax.set_ylabel('Datos analogos')
                
            ani =  animation.FuncAnimation(fig,animate, fargs=(xdatos,ydatos))
            plt.show();
            
            
        except KeyboardInterrupt:
            break
        
        
def puerto_serial_H_T():
    
    ser = serial.Serial('/dev/ttyACM0',9600)
    ser.flushInput()
    fig = plt.figure()
    ax=fig.add_subplot(1,1,1)
    ax.grid(True)
    ax.set_title("Temperatura y Humedad")
    
    xdatos, ydatosT, ydatosH, datosTxt = [], [], [], []
    

    now = datetime.now()
    fecha =now.strftime('%d.%m.%Y')
    nombre = '/home/pi/Desktop/Proyecto/Historial Datos/Tem_Hum_' + fecha + '.txt'
    
    while True:
      
        try:
            
            lineBytes = ser.readline()
            line = lineBytes.decode('utf-8')
            
            
            def animate(i,xdatos,ydatos):
                
                datos = ser.readline()
                line = datos.decode('utf-8')
                v_tem = line.split(",")[1]
                v_hum = line.split(",")[2]
                datosTxt.append([float(v_tem), float(v_hum)])
                xdatos.append(i)
                ydatosT.append(float(v_tem))
                ydatosH.append(float(v_hum))
                np.savetxt(nombre,datosTxt)
                
                ax.plot(xdatos,ydatosT, color='b')
                ax.plot(xdatos,ydatosH, color='g')
                ax.legend(["Temperatura(°C)","Humedad (%)"])
                ax.set_xlabel('Segundos')
                ax.set_ylabel('Porcentaje / Grados centigrados')
            ani =  animation.FuncAnimation(fig,animate, fargs=(xdatos,[ydatosT, ydatosH]))
            plt.show();
            
            
        except KeyboardInterrupt:
            break
        

def inicio_sesion():
    
    global pantalla2
    pantalla2 = Toplevel(pantalla)
    pantalla2.geometry("400x250")
    pantalla2.config(bg="white")
    pantalla2.title("Inicio de sesión")
    
    Label(pantalla2, text="Por favor ingrese su usuario y contraseña a continuación:",bg="white").pack()
    Label(pantalla2, text="",bg="white").pack()
    
    global nombreusuario_verify
    global contrasenausuario_verify
    
    nombreusuario_verify=StringVar()
    contrasenausuario_verify=StringVar()
    
    global nombre_usuario_entry
    global contrasena_usuario_entry
    
    Label(pantalla2, text="Usuario",bg="white").pack()
    nombre_usuario_entry = Entry(pantalla2, textvariable=nombreusuario_verify)
    nombre_usuario_entry.pack()
    Label(pantalla2, bg="white").pack()
    
    Label(pantalla2, text="Contraseña",bg="white").pack()
    contrasena_usuario_entry = Entry(pantalla2, show="*",textvariable=contrasenausuario_verify)
    contrasena_usuario_entry.pack()
    Label(pantalla2, bg="white").pack()
    
    Button(pantalla2, text="Iniciar Sesión",bg="white", command=validacion_datos).pack()

def VerTxt(pos):
    contenido = os.listdir('Historial Datos')
    pathTxt = os.path.join('Historial Datos', contenido[pos])
    txt = open(pathTxt, "r", encoding="utf-8")
    contenidoTxt = txt.read().split("\n")
    ventanaTxt = Toplevel()
    ventanaTxt.geometry("450x350")
    ventanaTxt.title("Visualizar Archivo")

    scrollbar = Scrollbar(ventanaTxt)
    scrollbar.pack(side=RIGHT, fill=Y)

    listbox = Listbox(ventanaTxt, yscrollcommand=scrollbar.set)

    for x in contenidoTxt:
        listbox.insert(END, str(x))

    listbox.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar.config(command=listbox.yview)

def borrarTxt(pos):
    contenido = os.listdir('Historial Datos')
    pathTxt = os.path.join('Historial Datos', contenido[pos])
    aux2 = messagebox.askyesno(message="¿Desea eliminar el archivo " + contenido[pos] + "?", title="Eliminar Archivo")
    if aux2:
        os.remove(pathTxt)
        renderizar_doc()

def renderizar_doc():
    canvas = Canvas(pantalla3)
    canvas.configure(highlightthickness=0)
    canvas.grid(column=0, columnspan=2, row=0, sticky="nsew")

    scrolly = Scrollbar(pantalla3, orient=VERTICAL, command=canvas.yview)
    scrolly.grid(row=0, column=2, sticky=NS)
    canvas.configure(yscrollcommand=scrolly.set)

    aux = IntVar()

    contenido = os.listdir('Historial Datos')

    for i in range(len(contenido)):
        # Label(root, text=contenido[i]).grid(row=i, column=0, columnspan=2) command=lambda: VerTxt(i)
        rb = Radiobutton(canvas, text=contenido[i], variable=aux, value=i)#.grid(row=i, column=0)
        canvas.create_window(0, i*50, anchor='nw', window=rb, height=50)

    canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scrolly.set)

    btnVer = Button(pantalla3, text="Ver Archivo", command=lambda: VerTxt(aux.get()))
    btnVer.grid(row=2, column=0)

    btnBorrar = Button(pantalla3, text="Eliminar Archivo", command=lambda: borrarTxt(aux.get()), background="red")
    btnBorrar.grid(row=2, column=1)

def renderizar_est():
    canvas = Canvas(pantalla4)
    canvas.configure(highlightthickness=0)
    canvas.grid(column=0, columnspan=2, row=0, sticky="nsew")

    scrolly = Scrollbar(pantalla4, orient=VERTICAL, command=canvas.yview)
    scrolly.grid(row=0, column=2, sticky=NS)
    canvas.configure(yscrollcommand=scrolly.set)

    aux = IntVar()

    contenido = os.listdir('Historial Datos')

    for i in range(len(contenido)):
        # Label(root, text=contenido[i]).grid(row=i, column=0, columnspan=2) command=lambda: VerTxt(i)
        rb = Radiobutton(canvas, text=contenido[i], variable=aux, value=i)#.grid(row=i, column=0)
        canvas.create_window(0, i*50, anchor='nw', window=rb, height=50)

    canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scrolly.set)

    btnVer = Button(pantalla4, text="Ver Archivo", command=lambda: VerTxt(aux.get()))
    btnVer.grid(row=2, column=0)

def validacion_datos():
    bd=pymysql.connect(
        host="localhost",
        user="root",
        passwd="manager",
        db="login"     
        )
    fcursor=bd.cursor()
    
    fcursor.execute("SELECT password FROM Usuarios WHERE user='"+nombreusuario_verify.get()+"'and password='"+contrasenausuario_verify.get()+"'")
    
    if fcursor.fetchall():
        messagebox.showinfo(title="Inicio de sesion correcto", message="usuario y contraseña correcta")
        
        
        if nombreusuario_verify.get() == "docente":
        
            global pantalla3
            pantalla3 = Toplevel(pantalla2)
            pantalla3.geometry("400x350")
            pantalla3.config(bg="white")
            pantalla3.title("Historial de datos")
            
            renderizar_doc()
            
        else:
            global pantalla4
            pantalla4 = Toplevel(pantalla2)
            pantalla4.geometry("400x350")
            pantalla4.config(bg="white")
            
            renderizar_est()
        
    else:
        messagebox.showinfo(title="Inicio de sesion incorrecto", message="usuario y contraseña incorrecto")
        
    bd.close()
    
def abrirArchivo ():
    archivo = filedialog.askopenfilename(title = "abrir", initialdir="/home/pi/Desktop/Proyecto/Historial Datos")
    print(archivo)

def VerVideo(ruta):
    global video
    video = cv2.VideoCapture(ruta)
    visualizarVideo()

def visualizarVideo():
    global video
    ret, frame = video.read()

    if ret == True:
        etiqVideo.pack()
        btn4.pack()
        frame = imutils.resize(frame, width=640)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=im)
        etiqVideo.configure(image=img)
        etiqVideo.image = img
        etiqVideo.after(5, visualizarVideo)
    else:
        video.release()

def VerImagen(ruta):
    etiqVideo.pack()
    btn4.pack()
    src = cv2.imread(ruta, cv2.IMREAD_UNCHANGED)
    frame = cv2.resize(src, (640, 360))
    im = Image.fromarray(frame)
    img = ImageTk.PhotoImage(image=im)
    etiqVideo.configure(image=img)
    etiqVideo.image = img


def quitar():
    global video
    global ventanaVideo
    etiqVideo.pack_forget()
    btn4.pack_forget()
    if video != None:
        video.release()

def render():
    global video
    video = None
    global ventanaVideo
    ventanaVideo = Toplevel()
    ventanaVideo.title('Video de conexión sensores y pagina web')
    ventanaVideo.geometry("700x600")
    ventanaVideo.resizable(width=False, height=False)

    frame1 = Frame(ventanaVideo, bd=0, relief=SOLID) 
    frame1.pack(side='top', fill=X, padx=10, pady=20)

    l1 = Label(frame1, text="Video conexiones", justify=CENTER)

    l2 = Label(frame1, text="Imagen 1 conexiones y sistema")
    
    l3 = Label(frame1, text="Imagen 2 pagina web")

    btn1 = Button(frame1, text="Ver Video", command=lambda: VerVideo("video1.mp4"))

    btn2 = Button(frame1, text="Ver Imagen", command=lambda: VerImagen("1.jpg"))
    
    btn3 = Button(frame1, text="Ver Imagen", command=lambda: VerImagen("2.jpg"))


    l1.grid(row=0, column=0, padx=50)
    l2.grid(row=1, column=0, padx=50)
    l3.grid(row=2, column=0, padx=50)
    
    btn1.grid(row=0, column=1, padx=20)
    btn2.grid(row=1, column=1, padx=20)
    btn3.grid(row=2, column=1, padx=20)

    frame2 = Frame(ventanaVideo, bd=0, relief=SOLID) 
    frame2.pack(side='bottom', expand=YES, fill=BOTH)
    global etiqVideo
    etiqVideo = Label(frame2)
    etiqVideo.pack()
    global btn4
    btn4 = Button(frame2, text="Quitar", command=quitar)


menu_pantalla()
    
    
    



