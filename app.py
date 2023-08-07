import time
import shutil
from os import path, listdir, mkdir
from tkinter import Tk, Label, Frame, messagebox, DISABLED, PhotoImage, Menu, Toplevel, filedialog, BooleanVar
from tkinter import ttk
from datetime import datetime

_CURRENT_DIR = path.dirname(path.abspath(__file__))
_TEST_DIR = path.join(_CURRENT_DIR,"Test")

class VentanaPrincipal(Tk):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_iu()
        self.create_widgets()
        self.init_icons()
    
    def init_iu(self):
        self.geometry(f"500x55+0+0") # Establecer las dimensiones y la posición de la ventana
        self.resizable(False, False)# Deshabilitar el redimensionamiento de la ventana
        self.title("Organizador")
    
    def init_icons(self):
        pass
    
    def create_widgets(self):
        self.lbl_title = Label(self, text='Organizador de Archivos')
        self.lbl_title.place(y=5, width=485)
        self.lbl_description = Label(self, text='?')
        self.lbl_description.place(x=485, y=5, width=5)
        self.lbl_description.bind("<Enter>", self.show_tooltip)
        self.lbl_description.bind("<Leave>", self.hide_tooltip)
        self.txt_path_carpeta = ttk.Entry(self)
        self.txt_path_carpeta.place(x=5, y=25, height=25, width=400)
        self.btn_open_folder = ttk.Button(self, text="...", command=self.open_folder)
        self.btn_open_folder.place(x=410, y=25, height=25, width=25)
        self.btn_analitic_folder = ttk.Button(self, text="A", command=self.create_list_checkbox)
        self.btn_analitic_folder.place(x=440, y=25, height=25, width=25)
        self.btn_process = ttk.Button(self, text="P", command=self.procesar)
        self.btn_process.place(x=470, y=25, height=25, width=25)
        self.btn_minimized_frame = ttk.Button(self, text=">>", command=self.minimized_frame)
        self.fr_analitic = Frame(self)
        self.fr_description = Frame(self)
    
    def show_tooltip(self, event):
        self.tooltip = Toplevel(self)
        self.tooltip.overrideredirect(True)
        self.tooltip.geometry(f"+{event.x_root+10}+{event.y_root+10}")  # Posición relativa al cursor
        tooltip_label = Label(self.tooltip, text="Este programa organiza todos los\n archivos por carpetas, segun el ultimo\n año en el que fue modificado.", justify='left')
        tooltip_label.pack()

    def hide_tooltip(self, event):
        self.tooltip.destroy()

    def procesar(self):
        for i, var in enumerate(self.variables):
            if var.get():
                self.create_folder(name_folder=f'{self.list_anio[i]}')
                self.mover_archivos(self.list_anio[i])
                #print(f'{self.list_anio[i]}: {"Marcada" if var.get() else "No marcada"}')

    def mover_archivos(self, folder_name:str):
        general_path = self.txt_path_carpeta.get()
        if path.exists(general_path):
            contenido = listdir(general_path)
            for archivo in contenido:
                if archivo not in self.list_anio:
                    ruta_archivo = path.join(general_path, archivo)
                    T_stamp = self.anio_modified_file(ruta_archivo)
                    if T_stamp  == folder_name:
                        directorio_especifico = path.join(general_path, T_stamp)
                        if path.exists(directorio_especifico):
                            new_ruta_archivo = path.join(directorio_especifico, archivo)
                            shutil.move(ruta_archivo, new_ruta_archivo)
                            print(f"Archivo: {archivo}, copiado con exito a nueva ruta {new_ruta_archivo}")
                        else:
                            print(f"Directorio: {directorio_especifico}, no encontrado")
        else:
            print(f"La ruta {folder_name}, no existe")

    def create_folder(self, name_folder:str):
        general_path = path.join(self.txt_path_carpeta.get())
        if path.exists(general_path):
            new_folder = path.join(general_path, name_folder)
            if not path.exists(new_folder):
                mkdir(new_folder)
                print(f"nueva carpeta: {new_folder}")
            else:
                print(f"La carpeta {new_folder}, ya existe")
        else:
            print(f"La ruta {general_path}, no existe")

    def create_list_checkbox(self):
        self.list_anio = []
        self.variables = []
        self.checkboxes = []
        self.list_anio = self.analitic_folder()
        self.list_anio.sort(key=int, reverse=True)
        self.geometry(f"500x{85+(len(self.list_anio)*30)}+0+0")
        self.btn_minimized_frame.place(x=5, y=55, height=20, width=490)
        self.fr_analitic.place(x=0, y=85, height=(len(self.list_anio)*30), width=245)
        self.fr_description.place(x=255, y=85, height=(len(self.list_anio)*30), width=245)
        for i, anio in enumerate(self.list_anio): # Crear una variable booleana para cada anio 
            var = BooleanVar() 
            self.variables.append(var) # Crear un checkbox para cada anio 
            check = ttk.Checkbutton(self.fr_analitic, text=anio, variable=var) 
            self.checkboxes.append(check) # Colocar el checkbox en la ventana usando place 
            check.place(x=5, y=(i*25))        

    def open_folder(self):
        new_path = filedialog.askdirectory()
        old_path = self.txt_path_carpeta.get()
        if new_path != old_path:
            self.txt_path_carpeta.delete(0, "end")
            self.txt_path_carpeta.insert(0, path.join(new_path))

    def minimized_frame(self):
        self.fr_analitic.place_forget()
        self.geometry(f"500x55+0+0")

    def analitic_folder(self) -> list:
        '''Devuelve la lista de los años donde fueron modificados los archivos'''
        try:
            folder_path = self.txt_path_carpeta.get()
            files = listdir(folder_path)
            list_anios = list()
            for file in files:
                file_path = path.join(folder_path, file)
                anio_modified = self.anio_modified_file(file_path)
                if anio_modified not in list_anios:
                    list_anios.append(anio_modified)
            return list_anios
        except Exception as ex:
            return print(ex)

    def anio_modified_file(self, file:str) -> str:
        '''Retorna el año en que el archivo fue modificado por ultima vez'''
        ruta_archivo = path.join(file)
        ti_m = path.getmtime(ruta_archivo) # fecha de modificacion del archivo
        m_ti = time.ctime(ti_m) # convierte el tiempo en segundos
        t_obj = time.strptime(m_ti) # crea una estructura en formato de tiempo
        T_stamp = time.strftime("%Y", t_obj) # transforma el formato
        return T_stamp
    
if __name__ == "__main__":
    ventana_principal = VentanaPrincipal()
    ventana_principal.mainloop()

# frutas = [“Manzana”, “Plátano”, “Naranja”, “Fresa”] 
# variables = [] 
# checkboxes = []

# for i, fruta in enumerate(frutas): # Crear una variable booleana para cada fruta 
#     var = tk.BooleanVar() 
#     variables.append(var) # Crear un checkbox para cada fruta 
#     check = ttk.Checkbutton(master, text=fruta, variable=var) 
#     checkboxes.append(check) # Colocar el checkbox en la ventana usando grid 
#     check.grid(row=i, column=0, sticky=“w”)