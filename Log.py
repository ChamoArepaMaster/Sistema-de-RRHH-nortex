from pathlib import Path
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import psycopg2

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def connect_to_database():
    """Establece conexión con la base de datos PostgreSQL"""
    try:
        connection = psycopg2.connect(
            host="25.40.205.49",  
            database="postgres".encode('utf-8').decode('utf-8'),
            user="Mamon".encode('utf-8').decode('utf-8'),
            password="7sonmasque6".encode('utf-8').decode('utf-8'),
            client_encoding='utf8'
        )
        return connection
    except psycopg2.Error as e:
        print(f"Error conectando a la base de datos: {e}")
        return None

def authenticate_user(username, password):
    """Autentica usuario contra la base de datos"""
    connection = connect_to_database()
    if not connection:
        return False, "Error de conexión a la base de datos"
    
    try:
        cursor = connection.cursor()
        query = "SELECT usuario, contrasena FROM usuarios WHERE usuario = %s AND contrasena = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        if result:
            return True, "Login exitoso"
        else:
            return False, "Usuario o contraseña incorrectos"
            
    except psycopg2.Error as e:
        return False, f"Error en la consulta: {e}"

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Nortex - Login")
        self.geometry("1194x639")
        self.minsize(800, 500)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=9)  # Logo section - increased weight
        self.grid_columnconfigure(1, weight=2)  # Login panel - decreased weight
        
        # Variables
        self.show_password = ctk.BooleanVar(value=False)
        self.error_label = None
        
        self.create_widgets()
        
        # Bind Enter key to login
        self.bind('<Return>', lambda event: self.handle_login())
    
    def create_widgets(self):
        self.logo_frame = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=0
        )
        self.logo_frame.grid(row=0, column=0, sticky="nsew")
        
        try:
            logo_path = relative_to_assets("nortex_logo.png")
            logo_pil = Image.open(logo_path)
            self.logo_image = ctk.CTkImage(
                light_image=logo_pil,
                size=(400, 300)
            )
            self.logo_label = ctk.CTkLabel(
                self.logo_frame,
                image=self.logo_image,
                text=""
            )
            self.logo_label.place(relx=0.5, rely=0.5, anchor="center")
        except Exception as e:
            print(f"[v0] Error loading logo: {e}")
            # Si no se encuentra la imagen, mostrar texto
            self.logo_label = ctk.CTkLabel(
                self.logo_frame,
                text="BONDEADOS\nnortex",
                font=("Arial", 48, "bold"),
                text_color="#D02F28"
            )
            self.logo_label.place(relx=0.5, rely=0.5, anchor="center")
        
        self.login_frame = ctk.CTkFrame(
            self,
            fg_color="#1A1464",
            corner_radius=0
        )
        self.login_frame.grid(row=0, column=1, sticky="nsew")
        
        self.login_frame.grid_rowconfigure(0, weight=1)
        self.login_frame.grid_rowconfigure(1, weight=0)
        self.login_frame.grid_rowconfigure(2, weight=0)
        self.login_frame.grid_rowconfigure(3, weight=0)
        self.login_frame.grid_rowconfigure(4, weight=0)
        self.login_frame.grid_rowconfigure(5, weight=0)
        self.login_frame.grid_rowconfigure(6, weight=1)
        self.login_frame.grid_columnconfigure(0, weight=1)
        
        self.username_entry = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Nombre de usuario",
            fg_color="#FFFFFF",
            text_color="#000000",
            placeholder_text_color="gray",
            border_color="#D02F28",
            border_width=2,
            corner_radius=5,
            height=40,
            width=350
        )
        self.username_entry.grid(row=1, column=0, padx=30, pady=(20, 10))
        
        self.password_entry = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Contraseña",
            show="*",
            fg_color="#FFFFFF",
            text_color="#000000",
            placeholder_text_color="gray",
            border_color="#D02F28",
            border_width=2,
            corner_radius=5,
            height=40,
            width=350
        )
        self.password_entry.grid(row=2, column=0, padx=30, pady=10)
        
        self.show_password_checkbox = ctk.CTkCheckBox(
            self.login_frame,
            text="Mostrar Contraseña",
            variable=self.show_password,
            command=self.toggle_password,
            fg_color="#D02F28",
            hover_color="#B02820",
            border_color="#D02F28",
            text_color="#D02F28",
            font=("Arial", 12)
        )
        self.show_password_checkbox.grid(row=3, column=0, padx=62, pady=10)
        
        self.login_button = ctk.CTkButton(
            self.login_frame,
            text="Inicio de sesión",
            command=self.handle_login,
            fg_color="#FFFFFF",
            text_color="#000000",
            hover_color="#F0F0F0",
            border_color="#D02F28",
            border_width=3,
            corner_radius=5,
            height=40,
            width=20,
            font=("Arial", 14, "bold")
        )
        self.login_button.grid(row=4, column=0, padx=30, pady=20)
        
        self.error_frame = ctk.CTkFrame(
            self.login_frame,
            fg_color="transparent"
        )
        self.error_frame.grid(row=5, column=0, padx=30, pady=5, sticky="ew")
        self.error_frame.grid_remove()
    
    def toggle_password(self):
        """Alterna la visibilidad de la contraseña"""
        if self.show_password.get():
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")
    
    def show_error_message(self, message):
        """Muestra mensaje de error en la interfaz"""
        self.error_frame.grid()
        
        # Limpiar frame de error
        for widget in self.error_frame.winfo_children():
            widget.destroy()
        
        error_container = ctk.CTkFrame(
            self.error_frame,
            fg_color="#FFFFFF",
            border_color="#D02F28",
            border_width=2,
            corner_radius=5
        )
        error_container.pack(fill="x", padx=5, pady=5)
        
        error_label = ctk.CTkLabel(
            error_container,
            text=f"⚠ {message}",
            text_color="#D02F28",
            font=("Arial", 11)
        )
        error_label.pack(padx=10, pady=8)
    
    def hide_error_message(self):
        """Oculta el mensaje de error"""
        self.error_frame.grid_remove()
    
    def handle_login(self):
        """Maneja el proceso de login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Validar que no estén vacíos
        if username == "":
            self.show_error_message("Por favor ingrese un nombre de usuario")
            return
        
        if password == "":
            self.show_error_message("Por favor ingrese una contraseña")
            return
        
        # Intentar autenticación
        success, message = authenticate_user(username, password)
        
        if success:
            self.hide_error_message()
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
            # Aquí puedes agregar código para abrir la siguiente ventana
        else:
            self.show_error_message("Acceso denegado: verifique su usuario y su contraseña")

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    app = LoginApp()
    app.mainloop()
