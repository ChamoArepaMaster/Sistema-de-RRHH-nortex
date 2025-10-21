from pathlib import Path
import customtkinter as ctk

# Configuración de rutas para assets
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"E:\Sistema\Logeo\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Configuración de CustomTkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class NortexApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema Nortex")
        self.geometry("1188x630")
        self.minsize(800, 500)
        self.resizable(True, True)        
        
        
      
        self.create_widgets()
    def abrir_emergente(self, titulo: str, mensaje: str):
        """Abre una ventana emergente con título y mensaje"""
        ventana = ctk.CTkToplevel(self)
        ventana.title(titulo)
        ventana.geometry("300x150")
        ventana.configure(fg_color="#F5F5F5")
        
        # Centrar la ventana
        ventana.transient(self)
        ventana.grab_set()
        
        label = ctk.CTkLabel(
            ventana,
            text=mensaje,
            font=("Arial", 12),
            text_color="#000000"
        )
        label.pack(expand=True, pady=30)
        
        btn_cerrar = ctk.CTkButton(
            ventana,
            text="Cerrar",
            command=ventana.destroy,
            fg_color="#1A1464",
            text_color="white",
            hover_color="#2A2474"
        )
        btn_cerrar.pack(pady=10)

    def create_widgets(self):
        self.top_frame = ctk.CTkFrame(
            self,
            height=117,
            fg_color="#1A1464",
            corner_radius=0
        )
        self.top_frame.pack(fill="x", side="top")
        self.top_frame.pack_propagate(False)
        
        self.buttons_frame = ctk.CTkFrame(
            self.top_frame,
            fg_color="transparent"
        )
        self.buttons_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Botón 1: Reporte Diario
        self.btn_reporte_diario = self.create_icon_button(
            self.buttons_frame,
            "Reporte Diario",
            "button_1.png",
            lambda: self.abrir_emergente("Reporte Diario", "bro")
        )
        self.btn_reporte_diario.grid(row=0, column=0, padx=10)
        
        # Botón 2: Vac/Pen
        self.btn_vac_pen = self.create_icon_button(
            self.buttons_frame,
            "Vac/Pen",
            "button_2.png",
            lambda: self.abrir_emergente("Vacaciones/Pendientes", "hola")
        )
        self.btn_vac_pen.grid(row=0, column=1, padx=10)
        
        # Botón 3: Estado
        self.btn_estado = self.create_icon_button(
            self.buttons_frame,
            "Estado",
            "button_3.png",
            lambda: self.abrir_emergente("Estado", "hola bro")
        )
        self.btn_estado.grid(row=0, column=2, padx=10)
        
        # Botón 4: Comprobante
        self.btn_comprobante = self.create_icon_button(
            self.buttons_frame,
            "Comprobante",
            "button_4.png",
            lambda: self.abrir_emergente("Comprobante", "pruebaaaa")
        )
        self.btn_comprobante.grid(row=0, column=3, padx=10)
        
        # Botón 5: Lista Empleados
        self.btn_lista_empleados = self.create_icon_button(
            self.buttons_frame,
            "Lista Empleados",
            "button_5.png",
            lambda: self.abrir_emergente("Lista Empleados", "pruebaaa")
        )
        self.btn_lista_empleados.grid(row=0, column=4, padx=10)
        
        # Botón 6: Lista de Usuarios
        self.btn_lista_usuarios = self.create_icon_button(
            self.buttons_frame,
            "Lista de Usuarios",
            "button_6.png",
            lambda: self.abrir_emergente("Lista de Usuarios", "bro")
        )
        self.btn_lista_usuarios.grid(row=0, column=5, padx=10)
        
        # Botón 7: Configuración
        self.btn_configuracion = self.create_icon_button(
            self.buttons_frame,
            "Configuración",
            "button_7.png",
            lambda: self.abrir_emergente("Configuración", "bro")
        )
        self.btn_configuracion.grid(row=0, column=6, padx=10)
        
        # Frame central para el logo
        self.center_frame = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF"
        )
        self.center_frame.pack(expand=True, fill="both")
        
        # Logo de Nortex (imagen central)
        try:
            self.logo_image = ctk.CTkImage(
                light_image=self.load_image("image_1.png"),
                size=(600, 300)
            )
            self.logo_label = ctk.CTkLabel(
                self.center_frame,
                image=self.logo_image,
                text=""
            )
            self.logo_label.place(relx=0.5, rely=0.5, anchor="center")
        except Exception as e:
            print(f"Error loading logo: {e}")
            self.logo_label = ctk.CTkLabel(
                self.center_frame,
                text="BONDEADOS\nnortex",
                font=("Arial", 48, "bold"),
                text_color="#1A1464"
            )
            self.logo_label.place(relx=0.5, rely=0.5, anchor="center")
        
        self.btn_cerrar_sesion = ctk.CTkButton(
            self,
            text="Cerrar sesión",
            width=156,
            height=41,
            fg_color="#FFFFFF",
            text_color="#FF0000",
            border_width=2,
            border_color="#FF0000",
            hover_color="#FFE0E0",
            font=("Arial", 12, "bold"),
            command=self.cerrar_sesion
        )
        self.btn_cerrar_sesion.place(relx=0.95, rely=0.95, anchor="se")

    def create_icon_button(self, parent, text, image_name, command):
        """Crea un botón con icono arriba y texto abajo con animaciones"""
        btn_frame = ctk.CTkFrame(
            parent,
            fg_color="#FFFFFF",
            border_width=2,
            border_color="#000000",
            width=133,
            height=85
        )
        btn_frame.pack_propagate(False)
        
        # Intentar cargar la imagen
        try:
            icon_image = ctk.CTkImage(
                light_image=self.load_image(image_name),
                size=(45, 45)
            )
            icon_label = ctk.CTkLabel(
                btn_frame,
                image=icon_image,
                text=""
            )
            icon_label.pack(pady=(8, 0))
        except Exception as e:
            print(f"Error loading {image_name}: {e}")
            # Si no se puede cargar la imagen, mostrar un placeholder
            icon_label = ctk.CTkLabel(
                btn_frame,
                text="📄",
                font=("Arial", 28)
            )
            icon_label.pack(pady=(8, 0))
        
        # Etiqueta de texto
        text_label = ctk.CTkLabel(
            btn_frame,
            text=text,
            font=("Arial", 10, "bold"),
            text_color="#000000"
        )
        text_label.pack(pady=(2, 8))
        
        def on_enter(e):
            btn_frame.configure(fg_color="#F0F0F0", border_color="#1A1464")
        
        def on_leave(e):
            btn_frame.configure(fg_color="#FFFFFF", border_color="#000000")
        
        def on_click(e):
            # Efecto de presión
            btn_frame.configure(fg_color="#D0D0D0")
            self.after(100, lambda: btn_frame.configure(fg_color="#F0F0F0"))
            self.after(200, command)
        
        # Vincular eventos a todos los elementos
        for widget in [btn_frame, icon_label, text_label]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", on_click)
        
        return btn_frame
    
    def load_image(self, image_name):
        """Carga una imagen desde la carpeta assets"""
        from PIL import Image
        image_path = relative_to_assets(image_name)
        return Image.open(image_path)
    
    
    def cerrar_sesion(self):
        """Cierra la aplicación"""
        print("Cerrando sesión...")
        self.quit()

if __name__ == "__main__":
    app = NortexApp()
    app.mainloop()