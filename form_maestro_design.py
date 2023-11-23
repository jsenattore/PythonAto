import tkinter as tk
from tkinter import font
from tkinter import ttk
from config import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA
import util.util_ventana as util_ventana
import util.util_imagenes as util_img
import pickle
from datetime import datetime
import serial
import threading
import os
import pdb



class FormularioMaestroDesign(tk.Tk):

    def __init__(self):
        super().__init__()
        self.logo = util_img.leer_imagen("./imagenes/COBERFOX.jpg", (700, 250))
        self.perfil = util_img.leer_imagen("./imagenes/LOGOPNG.png", (150, 150))
        self.config_window()
        self.paneles()
        self.controles_barra_superior()
        self.controles_menu_lateral()
        self.controles_cuerpo()


        "/////////////////////"
        self.peso_actual = tk.StringVar()
        self.peso_actual.set("0")
        print(self.peso_actual.get())
        self.entry_peso_actual = None  # Añade esta línea
        self.matriculas_pesadas = []
        self.peso_actual_editable = tk.StringVar(value="0")  # Inicializa la variable StringVar
        self.peso_actual_segunda_pesada = tk.StringVar(value="0")

        # Inicializa las variables asociadas a matrícula
        self.empresa_matricula = {}
        self.producto_matricula = {}
        self.chofer_matricula = {}
        self.observaciones_matricula = {}

        self.datos_pesadas = []
        self.matriculas_pesadas = self.obtener_matriculas_pesadas()

        self.cargar_datos()

        "/////////////////////"




    def config_window(self):
        # Configuración inicial de la ventana
        self.title('Sistema De Pesaje')
        self.iconbitmap("./imagenes/LOGOPNG.ico")
        w, h = 1024, 600
        util_ventana.centrar_ventana(self, w, h)

    def paneles(self):
         # Crear paneles: barra superior, menú lateral y cuerpo principal
        self.barra_superior = tk.Frame(
            self, bg=COLOR_BARRA_SUPERIOR, height=50)
        self.barra_superior.pack(side=tk.TOP, fill='both')

        self.menu_lateral = tk.Frame(self, bg=COLOR_MENU_LATERAL, width=150)
        self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False)

        self.cuerpo_principal = tk.Frame(
            self, bg=COLOR_CUERPO_PRINCIPAL)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)

    def controles_barra_superior(self):
        # Configuración de la barra superior
        font_awesome = font.Font(family='FontAwesome', size=12)

        # Etiqueta de título
        self.labelTitulo = tk.Label(self.barra_superior, text="Coberfox.SA")
        self.labelTitulo.config(fg="#fff", font=(
            "Roboto", 15), bg=COLOR_BARRA_SUPERIOR, pady=10, width=16)
        self.labelTitulo.pack(side=tk.LEFT)

        # Botón del menú lateral
        self.buttonMenuLateral = tk.Button(self.barra_superior, text="\uf0c9", font=font_awesome,
                                           command=self.toggle_panel, bd=0, bg=COLOR_BARRA_SUPERIOR, fg="white")
        self.buttonMenuLateral.pack(side=tk.LEFT)

        # Etiqueta de informacion
        self.labelTitulo = tk.Label(
            self.barra_superior, text="jsenattore@gmail.com")
        self.labelTitulo.config(fg="#fff", font=(
            "Roboto", 10), bg=COLOR_BARRA_SUPERIOR, padx=10, width=20)
        self.labelTitulo.pack(side=tk.RIGHT)

    def controles_menu_lateral(self):
        # Configuración del menú lateral
        ancho_menu = 20
        alto_menu = 2
        font_awesome = font.Font(family='FontAwesome', size=15)

         # Etiqueta de perfil
        self.labelPerfil = tk.Label(
            self.menu_lateral, image=self.perfil, bg=COLOR_MENU_LATERAL)
        self.labelPerfil.pack(side=tk.TOP, pady=10)

        # Botones del menú lateral

        self.buttonDashBoard = tk.Button(self.menu_lateral)
        self.buttonProfile = tk.Button(self.menu_lateral)
        self.buttonPicture = tk.Button(self.menu_lateral)
        self.buttonInfo = tk.Button(self.menu_lateral)
        self.buttonSettings = tk.Button(self.menu_lateral)

        buttons_info = [
            ("Dashboard", "\uf109", self.mostrar_dashboard),
            ("Profile", "\uf007", self.mostrar_perfil),
            ("Picture", "\uf03e", self.mostrar_picture),
            ("Info", "\uf129", self.mostrar_info),
            ("Settings", "\uf013", self.configuracion)
        ]

        for text, icon, command in buttons_info:
            # Define la variable 'button' antes de pasarla a la función 'configurar_boton_menu'
            button = tk.Button(self.menu_lateral, command=command)
            self.configurar_boton_menu(button, text, icon, font_awesome, ancho_menu, alto_menu, command)

    def controles_cuerpo(self):
        # Imagen en el cuerpo principal
        label = tk.Label(self.cuerpo_principal, image=self.logo,
                         bg=COLOR_CUERPO_PRINCIPAL)
        label.place(x=0, y=0, relwidth=1, relheight=1)

    def configurar_boton_menu(self, button, text, icon, font_awesome, ancho_menu, alto_menu, command):
        button.config(text=f"  {icon}    {text}", anchor="w", font=font_awesome,
                      bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=ancho_menu, height=alto_menu,
                      command=command)
        button.pack(side=tk.TOP)
        self.bind_hover_events(button)

    def bind_hover_events(self, button):
        # Asociar eventos Enter y Leave con la función dinámica
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))

    def on_enter(self, event, button):
        # Cambiar estilo al pasar el ratón por encima
        button.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg='white')

    def on_leave(self, event, button):
        # Restaurar estilo al salir el ratón
        button.config(bg=COLOR_MENU_LATERAL, fg='white')

    def toggle_panel(self):
        # Alternar visibilidad del menú lateral
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
        else:
            self.menu_lateral.pack(side=tk.LEFT, fill='y')


    ("EMPIEZA LA MAGIA "
     "****************************************************************************************************************")

    def limpiar_cuerpo_principal(self):
        # Elimina todos los widgets del cuerpo principal
        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()

    def mostrar_dashboard(self):
        self.limpiar_cuerpo_principal()
        # Agrega aquí los widgets específicos para el dashboard

    def mostrar_perfil(self):


        self.limpiar_cuerpo_principal()

        etiquetas = ["Matricula", "Empresa", "Producto", "Chofer", "Cantidad de ejes", "Observaciones",
                     "Tara Declarada", "Fecha", "Hora", "Numero de Pesada", "Peso Actual"]
        entry_widgets = {}

        for i, etiqueta in enumerate(etiquetas):
            tk.Label(self.cuerpo_principal, text=etiqueta).grid(row=i, column=0, padx=10, pady=10, sticky=tk.W)

            if etiqueta == "Peso Actual":
                label_peso = tk.Label(self.cuerpo_principal, textvariable=self.peso_actual)
                label_peso.grid(row=i, column=1, padx=10, pady=10)
            elif etiqueta == "Fecha":
                label_fecha = tk.Label(self.cuerpo_principal, text=datetime.now().strftime('%Y-%m-%d'))
                label_fecha.grid(row=i, column=1, padx=10, pady=10)
            elif etiqueta == "Hora":
                label_hora = tk.Label(self.cuerpo_principal, text=datetime.now().strftime('%H:%M:%S'))
                label_hora.grid(row=i, column=1, padx=10, pady=10)
            elif etiqueta == "Numero de Pesada":
                label_numero_pesada = tk.Label(self.cuerpo_principal, text=str(len(self.datos_pesadas) + 1))
                label_numero_pesada.grid(row=i, column=1, padx=10, pady=10)
            elif etiqueta == "Matricula":
                entry_matricula = tk.Entry(self.cuerpo_principal)
                entry_matricula.grid(row=i, column=1, padx=10, pady=10)
                entry_matricula.bind('<KeyRelease>',
                                     lambda event, combo=entry_matricula: self.actualizar_autocompletado(combo))

                entry_widgets[etiqueta] = entry_matricula
            else:
                entry = tk.Entry(self.cuerpo_principal, state="normal")
                entry.grid(row=i, column=1, padx=10, pady=10)
                entry_widgets[etiqueta] = entry

            try:
                ventana.unbind('<Double-Button-1>')
                ventana.bind('<Double-Button-1>',
                             lambda event, combo=entry_matricula, ventana=ventana: self.rellenar_campos(combo, ventana))
            except Exception as e:
                print(f"Error: {e}")
        print(self.peso_actual.get())


        btn_guardar_cambios = tk.Button(
            self.cuerpo_principal,
            text="Guardar Primera Pesada",
            command=lambda: self.guardar_primera_pesada(entry_widgets)
        )
        btn_guardar_cambios.grid(row=len(etiquetas), column=0, columnspan=2, pady=20)

        # Cambiar el texto de la etiqueta "Peso Actual" a "Bruto"
        self.peso_actual.set("Bruto")

    def cargar_datos_desde_archivo(self):
        # Obtén la ruta del script actual
        script_dir = os.path.dirname(os.path.realpath(__file__))

        # Construye la ruta al archivo 'datos_pesadas.pkl'
        file_path = os.path.join(script_dir, 'datos_pesadas.pkl')

        try:
            with open(file_path, 'rb') as file:
                # Tu lógica de carga de datos desde el archivo
                datos_pesadas = pickle.load(file)
                print("Datos cargados exitosamente.")
        except FileNotFoundError:
            print(f"El archivo '{file_path}' no se encontró. Creando uno nuevo...")

            # Aquí coloca tu lógica para inicializar datos_pesadas si el archivo no existe
            # Por ejemplo:
            datos_pesadas = []

            with open(file_path, 'wb') as file:
                pickle.dump(datos_pesadas, file)

            print("Archivo creado y datos iniciales guardados.")

    def guardar_primera_pesada(self, entry_widgets):
        # Obtener el valor de "Tara Declarada" del campo de entrada
        tara_declarada_str = entry_widgets["Tara Declarada"].get()

        # Convertir a entero, o asignar 0 si está vacío o no es convertible
        try:
            tara_declarada = int(tara_declarada_str) if tara_declarada_str else 0
        except ValueError:
            tara_declarada = 0

        nueva_pesada = {
            'Numero_Pesada': len(self.datos_pesadas) + 1,
            'Fecha_Hora': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Matricula': entry_widgets["Matricula"].get(),
            'Empresa': entry_widgets["Empresa"].get(),
            'Producto': entry_widgets["Producto"].get(),
            'Chofer': entry_widgets["Chofer"].get(),
            'Cantidad de ejes': entry_widgets["Cantidad de ejes"].get(),
            'Observaciones': entry_widgets["Observaciones"].get(),
            'Tara Declarada': tara_declarada,
            'Bruto': self.peso_actual.get(),
            'Neto': str(int(self.peso_actual.get()) - tara_declarada),
            'Fecha_Hora_Segunda_Pesada': '',  # Inicializar la fecha de la segunda pesada
        }

        self.datos_pesadas.append(nueva_pesada)
        self.guardar_datos()

    def mostrar_picture(self):
        self.limpiar_cuerpo_principal()

        # Asegúrate de crear la entrada para "Tara Declarada"
        entry_widgets = {}
        entry_widgets["Tara Declarada"] = tk.Entry(self.cuerpo_principal)
        entry_widgets["Tara Declarada"].grid(row=5, column=1, padx=10, pady=10)  # Ajusta la fila según sea necesario

        # Asegúrate de inicializar el evento de doble clic correctamente
        entry_matricula = tk.Entry(self.cuerpo_principal)
        entry_matricula.grid(row=0, column=1, padx=10, pady=10)
        entry_matricula.bind('<KeyRelease>', lambda event, combo=entry_matricula: self.actualizar_autocompletado(combo,
                                                                                                                 self.cuerpo_principal))
        entry_widgets["Matricula"] = entry_matricula

        self.setup_ventana_edicion(self.cuerpo_principal, entry_widgets)

    def mostrar_info(self):
        print(self.datos_pesadas)  # Agrega esta línea para verificar si hay datos
        self.limpiar_cuerpo_principal()
        self.cargar_datos_desde_archivo()

        tree = ttk.Treeview(self.cuerpo_principal, show="headings", height=5)
        print("Treeview creado")  # Agrega esta línea para verificar la creación del Treeview
        tree["columns"] = ("Nº", "Matricula", "Empresa", "Producto", "Observaciones",
                           "Cantidad de Ejes", "Bruto", "Tara Declarada", "Neto", "Fecha 1º Pesada", "Fecha 2º Pesada")

        columnas = ["Nº", "Matrícula", "Empresa", "Producto", "Observaciones",
                    "Cantidad de Ejes", "Bruto", "Tara Declarada", "Neto", "Fecha 1º Pesada", "Fecha 2º Pesada"]

        for column in tree["columns"]:
            tree.heading(column, text=column)
            tree.column(column, width=120, anchor=tk.CENTER)

        for pesada in self.datos_pesadas:
            numero_pesada = pesada.get("Numero_Pesada", "")
            matricula = pesada.get("Matricula", "")
            empresa = pesada.get("Empresa", "")
            producto = pesada.get("Producto", "")
            observaciones = pesada.get("Observaciones", "")
            cantidad_ejes = pesada.get("Cantidad de ejes", "")
            bruto = pesada.get("Bruto", "")
            tara = pesada.get("Tara Declarada", "")
            neto = pesada.get("Neto", "")
            fecha_primera_pesada = pesada.get("Fecha_Hora", "")
            fecha_segunda_pesada = pesada.get("Fecha_Hora_Segunda_Pesada", "")


            # Convertir las fechas a objetos datetime
            if fecha_primera_pesada:
                fecha_primera_pesada = datetime.strptime(fecha_primera_pesada, '%Y-%m-%d %H:%M:%S')
            if fecha_segunda_pesada:
                fecha_segunda_pesada = datetime.strptime(fecha_segunda_pesada, '%Y-%m-%d %H:%M:%S')

            print(f"Número de Pesada: {numero_pesada}")
            print(f"Matrícula: {matricula}")
            print(f"Fecha 1º Pesada: {fecha_primera_pesada}")
            print(f"Fecha 2º Pesada: {fecha_segunda_pesada}")

            tree.insert("", "end", values=(numero_pesada, matricula, empresa, producto, observaciones,
                                           cantidad_ejes, bruto, tara, neto,
                                           fecha_primera_pesada.strftime(
                                               '%Y-%m-%d %H:%M:%S') if fecha_primera_pesada else "",
                                           fecha_segunda_pesada.strftime(
                                               '%Y-%m-%d %H:%M:%S') if fecha_segunda_pesada else ""))



        tree.pack(expand=tk.YES, fill=tk.BOTH)
        self.cuerpo_principal.grab_release()

    def configuracion(self):
        self.limpiar_cuerpo_principal()
        tk.Label(self.cuerpo_principal, text="Puerto COM:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        entry_puerto = tk.Entry(self.cuerpo_principal)
        entry_puerto.insert(0, "COM1")
        entry_puerto.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.cuerpo_principal, text="Velocidad de baudios:").grid(row=1, column=0, padx=10, pady=10,
                                                                                sticky=tk.W)
        entry_baudios = tk.Entry(self.cuerpo_principal)
        entry_baudios.insert(0, "9600")
        entry_baudios.grid(row=1, column=1, padx=10, pady=10)

        btn_guardar_configuracion = tk.Button(self.cuerpo_principal, text="Guardar Configuración",
                                              command=lambda: self.guardar_configuracion(entry_puerto, entry_baudios))
        btn_guardar_configuracion.grid(row=2, column=0, columnspan=2, pady=20)
    def guardar_configuracion(self, entry_puerto, entry_baudios):
        puerto = entry_puerto.get()
        baudios = entry_baudios.get()
        print(f"Configuración guardada: Puerto {puerto}, Baudios {baudios}")
        threading.Thread(target=lambda: self.leer_puerto_COM(puerto, baudios)).start()


    "////////////////////////////////////"

    def cargar_datos(self):
        try:
            with open("datos_pesadas.pkl", "rb") as file:
                self.datos_pesadas = pickle.load(file)
        except (FileNotFoundError, pickle.UnpicklingError) as e:
            print(f"No se pudieron cargar los datos. Error: {e}")
            self.datos_pesadas = []

    def guardar_datos(self):
        with open("datos_pesadas.pkl", "wb") as file:
            pickle.dump(self.datos_pesadas, file)

    "////////////////////////////////////"

    def actualizar_peso_actual(self, datos):
        peso_entero = ''.join(filter(str.isdigit, datos))
        nuevo_peso = int(peso_entero) if peso_entero else 0

        print("Antes de actualizar, self.peso_actual:", nuevo_peso)

        if isinstance(self.peso_actual, tk.StringVar):
            self.peso_actual.set(str(nuevo_peso))

    def leer_puerto_COM(self, puerto, velocidad):
        ser = None
        try:
            ser = serial.Serial(puerto, int(velocidad))
            while True:
                datos = ser.readline().decode('utf-8').strip()
                self.after(100, self.actualizar_peso_actual, datos)
        except serial.SerialException as e:
            print(f"Error al abrir el puerto COM: {e}")
        finally:
            if ser and ser.is_open:
                ser.close()

    def start_serial_thread(self):
        threading.Thread(target=self.leer_puerto_COM, args=("COM1", "9600")).start()

    def guardar_pesada(self, entry_widgets):
        # Obtener el valor de "Tara Declarada" del campo de entrada
        tara_declarada_str = entry_widgets["Tara Declarada"].get()

        # Convertir a entero, o asignar 0 si está vacío o no es convertible
        try:
            tara_declarada = int(tara_declarada_str) if tara_declarada_str else 0
        except ValueError:
            tara_declarada = 0

        matricula = entry_widgets["Matricula"].get()

        # Obtener la segunda pesada
        segunda_pesada = self.obtener_pesada_por_matricula(matricula)

        if segunda_pesada:
            # Actualizar los campos necesarios en la segunda pesada
            segunda_pesada['Chofer'] = entry_widgets["Chofer"].get()
            segunda_pesada['Empresa'] = entry_widgets["Empresa"].get()
            segunda_pesada['Producto'] = entry_widgets["Producto"].get()
            segunda_pesada['Observaciones'] = entry_widgets["Observaciones"].get()

            # Establecer la fecha solo en la segunda pesada si no tiene fecha
            if 'Fecha_Hora' not in segunda_pesada:
                segunda_pesada['Fecha_Hora'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            else:
                segunda_pesada['Fecha_Hora_Segunda_Pesada'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Verificar si la primera pesada existe
            pesada_primera = self.obtener_pesada_por_matricula(matricula)
            if pesada_primera:
                # Obtener Bruto y Tara de las pesadas
                bruto_primera_pesada = int(pesada_primera.get('Bruto', 0))
                bruto_segunda_pesada = int(self.peso_actual.get())

                # Determinar el mayor y el menor
                bruto_mayor = max(bruto_primera_pesada, bruto_segunda_pesada)
                bruto_menor = min(bruto_primera_pesada, bruto_segunda_pesada)

                # Actualizar Bruto, Tara y Neto en la segunda pesada
                segunda_pesada['Bruto'] = str(bruto_mayor)
                segunda_pesada['Tara Declarada'] = str(bruto_menor)
                segunda_pesada['Neto'] = str(bruto_mayor - bruto_menor)

        # Verificar si la matrícula tiene una primera pesada
        pesada_primera = self.obtener_pesada_por_matricula(matricula)

        if pesada_primera and 'Fecha_Hora' not in pesada_primera:
            # Actualizar Bruto y Tara de la primera pesada
            pesada_primera['Bruto'] = str(bruto_mayor)
            pesada_primera['Tara Declarada'] = str(bruto_menor)
            pesada_primera['Neto'] = str(bruto_mayor - bruto_menor)

        self.guardar_datos()

    def mostrar_sugerencias(self, ventana, sugerencias):
        # Limpiar el Listbox
        listbox_sugerencias = ventana.grid_slaves(row=0, column=2)[0]
        listbox_sugerencias.delete(0, tk.END)

        # Mostrar todas las sugerencias en el Listbox
        for sugerencia in sugerencias:
            # Obtener el número de pesada y la fecha asociada a la matrícula
            pesadas_asociadas = [p for p in self.datos_pesadas if p.get("Matricula", "").startswith(sugerencia)]

            for pesada_asociada in pesadas_asociadas:
                numero_pesada = pesada_asociada.get('Numero_Pesada', '')
                fecha_pesada = pesada_asociada.get('Fecha_Hora', '')
                sugerencia_texto = f"{sugerencia} - Pesada {numero_pesada} - Fecha: {fecha_pesada}"
                listbox_sugerencias.insert(tk.END, sugerencia_texto)
    def obtener_pesada_por_matricula(self, matricula):
        for pesada in self.datos_pesadas:
            if pesada.get("Matricula", "") == matricula:
                return pesada
        return None

    def obtener_tara_por_matricula(self, matricula):
        for pesada in self.datos_pesadas:
            if pesada.get("Matricula", "") == matricula:
                # Obtener la Tara Declarada y convertirla a entero
                tara_declarada_str = pesada.get("Tara Declarada", "0")
                try:
                    tara_declarada = int(tara_declarada_str)
                except ValueError:
                    tara_declarada = 0

                return tara_declarada

        # Si no se encuentra la matrícula, devolver 0
        return 0

    def rellenar_campos(self, entry, ventana):
        print("Entrando en rellenarcampos")

        # Obtén el Listbox correcto utilizando el método grid_slaves
        listbox_sugerencias = ventana.grid_slaves(row=0, column=2)[0]

        # Asegúrate de que se haya seleccionado un elemento en el Listbox
        if listbox_sugerencias.size() > 0:
            # Obtiene la matrícula seleccionada desde el Listbox
            matricula_seleccionada_full = listbox_sugerencias.get(tk.ACTIVE)
            matricula_seleccionada = matricula_seleccionada_full.split(' ')[0]  # Obtiene solo la matrícula

        # Obtiene el número de pesada desde la matrícula seleccionada
        numero_pesada = int(''.join(filter(str.isdigit, (matricula_seleccionada_full.split('-')[1].strip()))))
        print(numero_pesada)

        # Busca los datos correspondientes al número de pesada
        pesada_seleccionada = next((p for p in self.datos_pesadas if p.get('Numero_Pesada') == numero_pesada), None)

        # Si no se encuentra la pesada, salir
        if not pesada_seleccionada:
            return

        # Encuentra los Entry widgets en la ventana
        entry_widgets = {child.grid_info()["row"]: child for child in ventana.winfo_children() if
                         isinstance(child, tk.Entry)}

        # Itera sobre los Entry widgets y asigna valores según la posición
        for row, entry_widget in entry_widgets.items():
            if row == 0:  # Matrícula
                entry_widget.delete(0, tk.END)  # Borra el contenido actual
                entry_widget.insert(0, matricula_seleccionada)  # Asigna la matrícula
            elif row == 1:  # Empresa
                entry_widget.delete(0, tk.END)  # Borra el contenido actual
                entry_widget.insert(0, pesada_seleccionada.get("Empresa", ""))  # Asigna la empresa
            elif row == 2:  # Producto
                entry_widget.delete(0, tk.END)  # Borra el contenido actual
                entry_widget.insert(0, pesada_seleccionada.get("Producto", ""))  # Asigna el producto
            elif row == 3:  # Chofer
                entry_widget.delete(0, tk.END)  # Borra el contenido actual
                entry_widget.insert(0, pesada_seleccionada.get("Chofer", ""))  # Asigna el chofer
            elif row == 4:  # Observaciones
                entry_widget.delete(0, tk.END)  # Borra el contenido actual
                entry_widget.insert(0, pesada_seleccionada.get("Observaciones", ""))  # Asigna las observaciones

    def actualizar_autocompletado(self, entry, ventana):
        print("Entrando en actualizar_autocompletado")
        # Obtener el texto actual en el cuadro de entrada
        texto_actual = entry.get()
        # Más mensajes de impresión
        print(f"Text: {texto_actual}")

        # Actualizar la lista de matrículas cada vez que se escribe en el cuadro de entrada
        self.obtener_matriculas_pesadas()

        # Obtener el valor de Tara Declarada del campo de entrada
        slaves = ventana.grid_slaves(row=6, column=1)

        if slaves and isinstance(slaves[0], tk.Entry):
            tara_declarada_str = slaves[0].get()
        else:
            tara_declarada_str = ''

        try:
            tara_declarada = int(tara_declarada_str) if tara_declarada_str else 0
        except ValueError:
            # Manejar el caso en el que Tara Declarada no es un número válido
            tara_declarada = 0

        # Filtrar las matrículas que coinciden con el texto actual y tienen Tara igual a 0
        sugerencias = [matricula for matricula in self.matriculas_pesadas if matricula.startswith(texto_actual)
                       and self.obtener_tara_por_matricula(matricula) == 0]

        # Mostrar sugerencias en el Listbox
        self.mostrar_sugerencias(ventana, sugerencias)

        # Limpiar el evento de doble clic y volver a asociar la función de rellenar campos
        try:
            ventana.unbind('<Double-Button-1>')
            ventana.bind('<Double-Button-1>',
                         lambda event, combo=entry, ventana=ventana: self.rellenar_campos(combo, ventana))
        except Exception as e:
            print(f"Error: {e}")

    def setup_ventana_edicion(self, ventana, entry_widgets):
        etiquetas = ["Matricula", "Empresa", "Producto", "Chofer", "Observaciones"]

        entry_matricula = tk.Entry(ventana)
        entry_matricula.grid(row=0, column=1, padx=10, pady=10)
        entry_widgets["Matricula"] = entry_matricula

        for i, etiqueta in enumerate(etiquetas):
            tk.Label(ventana, text=etiqueta).grid(row=i, column=0, padx=10, pady=10, sticky=tk.W)

            if etiqueta == "Matricula":
                # ...
                entry_matricula = tk.Entry(ventana)
                entry_matricula.grid(row=i, column=1, padx=10, pady=10)
                entry_widgets[etiqueta] = entry_matricula
                # ...
                entry_tara_declarada = tk.Entry(ventana)
                entry_tara_declarada.grid(row=6, column=1, padx=10, pady=10)
                entry_widgets["Tara Declarada"] = entry_tara_declarada
                # ...
                print(entry_matricula)
                # Configurar evento de autocompletado
                entry_matricula.bind('<KeyRelease>',
                                     lambda event, combo=entry_matricula: self.actualizar_autocompletado(combo,
                                                                                                         ventana))
                # ...
            else:
                entry = tk.Entry(ventana)
                entry.grid(row=i, column=1, padx=10, pady=10)
                entry_widgets[etiqueta] = entry

        # Cuadro de 300x100 (en este caso, será un Listbox)
        listbox_sugerencias = tk.Listbox(ventana, width=50, height=5)
        listbox_sugerencias.grid(row=0, column=2, rowspan=len(etiquetas), padx=10, pady=10)

        # Cuadro de texto para el peso actual
        tk.Label(ventana, text="Peso Actual:").grid(row=len(etiquetas) + 2, column=0, padx=10, pady=10, sticky=tk.W)
        label_peso_actual_segunda_pesada = tk.Label(ventana, textvariable=self.peso_actual)
        label_peso_actual_segunda_pesada.grid(row=len(etiquetas) + 2, column=1, padx=10, pady=10)



        btn_guardar_cambios = tk.Button(
            ventana,
            text="Guardar Pesada",
            command=lambda: self.guardar_pesada(entry_widgets)
        )
        btn_guardar_cambios.grid(row=len(etiquetas) + 1, column=0, columnspan=3, pady=20)

        # Limpiar el evento de doble clic y volver a asociar la función de rellenar campos
        try:
            ventana.unbind('<Double-Button-1>')
            ventana.bind('<Double-Button-1>', lambda event, combo=entry_matricula, listbox=listbox_sugerencias,
                                                     ventana=ventana: self.rellenar_campos(combo, listbox, ventana))
        except Exception as e:
            print(f"Error: {e}")

    def obtener_matriculas_pesadas(self):
        matriculas = set()
        for pesada in self.datos_pesadas:
            matricula = pesada.get("Matricula", "")
            if matricula:
                matriculas.add(matricula)
        self.matriculas_pesadas = list(matriculas)
        return self.matriculas_pesadas

