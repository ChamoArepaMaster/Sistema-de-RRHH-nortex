from pathlib import Path
import psycopg2
from tkinter import messagebox

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Frame, Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"E:\Sistema\Logeo\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def connect_to_database():
    """Establece conexión con la base de datos PostgreSQL"""
    try:
        connection = psycopg2.connect(
            host="25.40.205.49",  
            database="prueba".encode('utf-8').decode('utf-8'),
            user="mamon".encode('utf-8').decode('utf-8'),
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

def handle_login():
    """Maneja el proceso de login"""
    username = entry_2.get()
    password = entry_1.get()
    
    # Validar que no estén vacíos o con placeholders
    if username == placeholder2 or username.strip() == "":
        show_error_message("Por favor ingrese un nombre de usuario")
        return
    
    if password == placeholder or password.strip() == "":
        show_error_message("Por favor ingrese una contraseña")
        return
    
    # Intentar autenticación
    success, message = authenticate_user(username, password)
    
    if success:
        hide_error_message()
        messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
        # Aquí puedes agregar código para abrir la siguiente ventana o funcionalidad
    else:
        show_error_message("Acceso denegado: verifique su usuario y su contraseña")

def show_error_message(message):
    """Muestra mensaje de error en la interfaz"""
    # Crear rectángulo de fondo para el mensaje de error
    canvas.create_rectangle(
        419.0, 60.0, 840.0, 120.0,
        fill="#FFFFFF", outline="#D02F28", width=2,
        tags="error_message"
    )
    canvas.create_text(
        445, 85, text="⚠", fill="#D02F28", 
        font=("Arial", 12, "bold"),
        tags="error_message"
    )
    
    # Crear texto del mensaje
    canvas.create_text(
        460.0, 90.0,
        anchor="w",
        text=message,
        fill="#000000",
        font=("Arial", 11),
        tags="error_message"
    )

def hide_error_message():
    """Oculta el mensaje de error"""
    canvas.delete("error_message")

window = Tk()

window.geometry("1194x639")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 639,
    width = 1194,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    515.0,
    320.0,
    image=image_image_1
)

canvas.create_rectangle(
    964.0,
    0.0,
    1194.0,
    639.0,
    fill="#1A1464",
    outline="")
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=2,
    highlightbackground="#D02F28",
    highlightcolor="#FF0303"
)
entry_1.place(
    x=1007.0,
    y=316.0,
    width=143.0,
    height=35.0
)
placeholder = "Contraseña"
entry_1.insert(0, placeholder)
entry_1.config(fg="gray")

def on_focus_in(event):
    if entry_1.get() == placeholder:
        entry_1.delete(0, "end")
        entry_1.config(fg="#000716")
    if not checkbox_checked[0]: 
        entry_1.config(show="*")

def on_focus_out(event):
    if entry_1.get() == "":
        entry_1.insert(0, placeholder)
        entry_1.config(fg="gray",show="")

entry_1.bind("<FocusIn>", on_focus_in)
entry_1.bind("<FocusOut>", on_focus_out)

entry_2 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=2,
    highlightbackground="#D02F28",
    highlightcolor="#FF0303"
)
entry_2.place(
    x=1007.0,
    y=228.0,
    width=143.0,
    height=35.0
)
placeholder2 = "Nombre de usuario"
entry_2.insert(0, placeholder2)
entry_2.config(fg="gray")

def on_focus_in2(event):
    if entry_2.get() == placeholder2:
        entry_2.delete(0, "end")
        entry_2.config(fg="#000716")

def on_focus_out2(event):
    if entry_2.get() == "":
        entry_2.insert(0, placeholder2)
        entry_2.config(fg="gray")

entry_2.bind("<FocusIn>", on_focus_in2)
entry_2.bind("<FocusOut>", on_focus_out2)

checkbox_rect = canvas.create_rectangle(
    1000.0,
    402.0,
    1020.0,
    420.0,
    fill="#FFFFFF",
    outline="#D02F28"
)

# Variable to track checkbox state
checkbox_checked = [False]  # Use list for mutability in nested function

def toggle_password(event):
    checkbox_checked[0] = not checkbox_checked[0]
    if checkbox_checked[0]:
        entry_1.config(show="")
        # Draw checkmark
        canvas.create_line(1004, 410, 1010, 416, fill="#D02F28", width=2, tag="checkmark")
        canvas.create_line(1010, 416, 1018, 404, fill="#D02F28", width=2, tag="checkmark")
    else:
        if entry_1.get() != placeholder:
            entry_1.config(show="*")
            # Remove checkmark
        canvas.delete("checkmark")

# Bind click event to the rectangle
canvas.tag_bind(checkbox_rect, "<Button-1>", toggle_password)

# Set password entry to hidden by default
entry_1.config(show="")

canvas.create_text(
    1023.0,
    403.0,
    anchor="nw",
    text="Mostrar contraseña",
    fill="#D02F28",
    font=("HammersmithOne Regular", 14 * -1)
)
border_frame = Frame(window, bg="red", highlightthickness=0)
border_frame.place(x=1013, y=457, width=128, height=25)
button_1 = Button(
    border_frame,
    text="Iniciar sesión",
    borderwidth=0,         # No internal border
    bg="#FFFFFF",          # Button background
    activebackground="#F0F0F0",
    command=handle_login,  # Updated to call login function
    relief="flat"
)
button_1.pack(fill="both", expand=True, padx=2, pady=2)

window.bind('<Return>', lambda event: handle_login())

window.resizable(False, False)
window.mainloop()
