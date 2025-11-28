import customtkinter as ctk
from tkinter import ttk
import tkinter as tk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class ListaUsuariosApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Lista usuarios")
        
        # Configurar tamaño inicial y adaptativo
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        window_width = 800
        window_height = 500
        
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.window.minsize(800, 600)
        
        # Colores personalizados (iguales al Reporte Diario)
        self.color_rojo = "#FF3333"
        self.color_blanco = "#FFFFFF"
        self.color_gris = "#F0F0F0"
        self.color_negro = "#000000"
        
        self.crear_layout()
    
    def crear_layout(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self.window, fg_color=self.color_blanco)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Barra de búsqueda
        search_frame = ctk.CTkFrame(main_frame, fg_color=self.color_blanco)
        search_frame.pack(fill="x", pady=(0, 20))
        
        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Barra de búsqueda",
            fg_color=self.color_blanco,
            text_color=self.color_negro,
            border_color=self.color_gris,
            border_width=2,
            height=40
        )
        search_entry.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Botón de búsqueda
        search_button = ctk.CTkButton(
            search_frame,
            text="🔍",
            width=40,
            height=40,
            fg_color=self.color_gris,
            text_color=self.color_negro,
            hover_color="#E0E0E0"
        )
        search_button.pack(side="left")
        
        # Frame para la tabla
        table_frame = ctk.CTkFrame(main_frame, fg_color=self.color_blanco)
        table_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Crear tabla con ttk.Treeview
        columns = (
            "Nombre de usuario",
            "Contraseña",
            "Tipo de cuenta"
        )
        
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            height=10,
            show="headings"
        )
        
        # Configurar encabezados
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=250, anchor="center")
        
        # Personalizar estilos de la tabla
        style = ttk.Style()
        style.theme_use("clam")
        
        # Estilo para el encabezado (rojo)
        style.configure("Treeview.Heading",
                       background=self.color_rojo,
                       foreground=self.color_negro,
                       font=("Arial", 10, "bold"),
                       relief="solid",
                       borderwidth=1)
        
        # Estilo para las filas
        style.configure("Treeview",
                       background=self.color_blanco,
                       foreground=self.color_negro,
                       fieldbackground=self.color_blanco,
                       font=("Arial", 9),
                       rowheight=30,
                       borderwidth=1,
                       relief="solid")
        
        style.map("Treeview", background=[("selected", "#CCCCCC")])

        
        # Agregar filas vacías
        for i in range(9):
            self.tree.insert("", "end", values=("",) * len(columns))
        
        self.tree.pack(fill="both", expand=True, side="left")
        
        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Frame de botones
        button_frame = ctk.CTkFrame(main_frame, fg_color=self.color_blanco)
        button_frame.pack(fill="x", pady=(20, 0))
        
        # Botón ELIMINAR
        btn_eliminar = ctk.CTkButton(
            button_frame,
            text="ELIMINAR",
            width=150,
            height=40,
            fg_color=self.color_blanco,
            text_color=self.color_negro,
            hover_color=self.color_gris,
            font=("Arial", 11, "bold"),
            border_width=2,
            border_color=self.color_rojo
        )
        btn_eliminar.pack(side="left", padx=10)
        
        # Botón AGREGAR
        btn_agregar = ctk.CTkButton(
            button_frame,
            text="AGREGAR",
            width=150,
            height=40,
            fg_color=self.color_blanco,
            text_color=self.color_negro,
            hover_color=self.color_gris,
            font=("Arial", 11, "bold"),
            border_width=2,
            border_color=self.color_rojo
        )
        btn_agregar.pack(side="right", padx=10)
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ListaUsuariosApp()
    app.run()
