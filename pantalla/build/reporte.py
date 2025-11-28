import customtkinter as ctk
from tkinter import ttk
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class DateDropdown(ctk.CTkFrame):
    """Dropdown personalizado que muestra fechas en un rango limitado"""
    def __init__(self, parent, values, command=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.values = values
        self.command = command
        self.selected_value = values[0] if values else ""
        self.visible_rows = 8
        self.popup = None

        self.button = ctk.CTkButton(
            self,
            text=self.selected_value,
            command=self.show_dropdown,
            fg_color="#FFFFFF",
            text_color="#000000",
            border_color="#FF3333",
            border_width=2,
            height=28,
            font=("Arial", 9)
        )
        self.button.pack(fill="both", expand=True)

    def show_dropdown(self):
        """Muestra el dropdown con las opciones en un rango limitado"""
        if self.popup:
            self.popup.destroy()

        self.popup = tk.Toplevel(self.master)
        self.popup.wm_overrideredirect(True)

        x = self.button.winfo_rootx()
        y = self.button.winfo_rooty() + self.button.winfo_height()
        self.popup.geometry(f"+{x}+{y}")

        frame = ttk.Frame(self.popup)
        frame.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        listbox = tk.Listbox(
            frame,
            yscrollcommand=scrollbar.set,
            font=("Arial", 9),
            height=self.visible_rows,
            width=15,
            highlightthickness=1,
            highlightcolor="#FF3333"
        )
        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=listbox.yview)

        for val in self.values:
            listbox.insert(tk.END, val)

        try:
            current_index = self.values.index(self.selected_value)
            listbox.selection_set(current_index)
            listbox.see(current_index)
        except ValueError:
            pass

        def on_select(event=None):
            selection = listbox.curselection()
            if selection:
                self.selected_value = self.values[selection[0]]
                self.button.configure(text=self.selected_value)
                if self.command:
                    self.command(self.selected_value)
                self.popup.destroy()
                self.popup = None

        def on_mousewheel(event):
            listbox.yview_scroll(int(-1*(event.delta/120)), "units")

        listbox.bind("<Double-Button-1>", on_select)
        listbox.bind("<Return>", on_select)
        listbox.bind("<MouseWheel>", on_mousewheel)
        listbox.bind("<Button-4>", lambda e: listbox.yview_scroll(-3, "units"))
        listbox.bind("<Button-5>", lambda e: listbox.yview_scroll(3, "units"))

        listbox.focus()

    def set(self, value):
        """Establece el valor seleccionado"""
        if value in self.values:
            self.selected_value = value
            self.button.configure(text=value)

    def get(self):
        """Obtiene el valor seleccionado"""
        return self.selected_value

class ReporteDiarioApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Reporte diario")

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        window_width = 800
        window_height = 500

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.window.minsize(800, 600)

        self.color_rojo = "#FF3333"
        self.color_blanco = "#FFFFFF"
        self.color_gris = "#F0F0F0"
        self.color_negro = "#000000"

        self.selected_date = datetime.now().strftime("%d/%m/%Y")
        
        # Variable para el widget de edición
        self.entry_popup = None

        self.crear_layout()

    def generar_fechas(self):
        """Genera lista de fechas desde hoy hasta el 1 de enero"""
        fecha_actual = datetime.now()
        fecha_inicio = datetime(fecha_actual.year, 1, 1)

        fechas = []
        fecha_actual_iter = fecha_actual

        while fecha_actual_iter >= fecha_inicio:
            fechas.append(fecha_actual_iter.strftime("%d/%m/%Y"))
            fecha_actual_iter -= timedelta(days=1)

        return fechas

    def on_date_selected(self, value):
        """Callback cuando se selecciona una fecha"""
        self.selected_date = value
        print(f"Fecha seleccionada: {self.selected_date}")

    # Nueva función para editar celdas
    def on_double_click(self, event):
        """Maneja el doble clic en una celda para editarla"""
        # Cerrar cualquier entrada anterior
        if self.entry_popup:
            self.entry_popup.destroy()

        # Identificar la región clickeada
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        # Obtener la columna y el item
        column = self.tree.identify_column(event.x)
        item = self.tree.identify_row(event.y)

        if not item or not column:
            return

        # Convertir el índice de columna de #1, #2, etc. a 0, 1, etc.
        column_index = int(column.replace('#', '')) - 1
        column_name = self.tree["columns"][column_index]

        # Obtener las coordenadas de la celda
        x, y, width, height = self.tree.bbox(item, column)

        # Obtener el valor actual
        current_value = self.tree.item(item)["values"][column_index]

        # Crear un Entry widget para editar
        self.entry_popup = tk.Entry(
            self.tree,
            font=("Arial", 9),
            justify="center"
        )
        self.entry_popup.place(x=x, y=y, width=width, height=height)
        self.entry_popup.insert(0, current_value)
        self.entry_popup.select_range(0, tk.END)
        self.entry_popup.focus()

        # Función para guardar el valor editado
        def save_edit(event=None):
            new_value = self.entry_popup.get()
            values = list(self.tree.item(item)["values"])
            values[column_index] = new_value
            self.tree.item(item, values=values)
            self.entry_popup.destroy()
            self.entry_popup = None
            print(f"Celda actualizada: {column_name} = {new_value}")

        # Función para cancelar la edición
        def cancel_edit(event=None):
            self.entry_popup.destroy()
            self.entry_popup = None

        # Bindings para guardar o cancelar
        self.entry_popup.bind("<Return>", save_edit)
        self.entry_popup.bind("<FocusOut>", save_edit)
        self.entry_popup.bind("<Escape>", cancel_edit)

    def grabar_datos(self):
        """Guarda los datos de la tabla en memoria"""
        datos = []
        for item in self.tree.get_children():
            valores = self.tree.item(item)["values"]
            # Solo guardar filas que tengan al menos un valor no vacío
            if any(str(v).strip() for v in valores):
                datos.append(valores)
        
        # Aquí podrías agregar lógica para guardar en base de datos u otro destino
        print(f"Datos guardados: {len(datos)} registros")
        messagebox.showinfo("Éxito", f"Se guardaron {len(datos)} registros en memoria")

    def exportar_datos(self):
        """Exporta los datos de la tabla"""
        datos = []
        for item in self.tree.get_children():
            valores = self.tree.item(item)["values"]
            if any(str(v).strip() for v in valores):
                datos.append(valores)
        
        print(f"Exportar datos: {len(datos)} registros")
        messagebox.showinfo("Exportar", f"Se exportarían {len(datos)} registros")

    def crear_layout(self):
        main_frame = ctk.CTkFrame(self.window, fg_color=self.color_blanco)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

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

        table_frame = ctk.CTkFrame(main_frame, fg_color=self.color_blanco)
        table_frame.pack(fill="both", expand=True, pady=(0, 20))

        columns = (
            "NOMBRE Y APELLIDO",
            "HORAS TRABAJADAS HOY",
            "HORAS DE ENFERMEDAD",
            "HORAS DE FERIADO",
            "LLEGADAS A TARDE",
            "OBSERVACIONES",
            "HORAS DE LICENCIA",
            "HORAS DE ART",
            "HORAS DE VACACIONES"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            height=10,
            show="headings"
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110, anchor="center")

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview.Heading",
                       background=self.color_rojo,
                       foreground=self.color_negro,
                       font=("Arial", 10, "bold"),
                       relief="solid",
                       borderwidth=1)

        style.configure("Treeview",
                       background=self.color_blanco,
                       foreground=self.color_negro,
                       fieldbackground=self.color_blanco,
                       font=("Arial", 9),
                       rowheight=30,
                       borderwidth=1,
                       relief="solid")

        style.map("Treeview", background=[("selected", "#CCCCCC")])

        for i in range(10):
            self.tree.insert("", "end", values=("",) * len(columns))

        # Agregar binding para doble clic
        self.tree.bind("<Double-Button-1>", self.on_double_click)

        self.tree.pack(fill="both", expand=True, side="left")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        button_frame = ctk.CTkFrame(main_frame, fg_color=self.color_blanco)
        button_frame.pack(fill="x", pady=(20, 0))

        btn_exportar = ctk.CTkButton(
            button_frame,
            text="EXPORTAR DATOS",
            width=150,
            height=40,
            fg_color=self.color_blanco,
            text_color=self.color_negro,
            hover_color=self.color_gris,
            font=("Arial", 11, "bold"),
            border_width=2,
            border_color=self.color_rojo,
            command=self.exportar_datos
        )
        btn_exportar.pack(side="left", padx=10)

        btn_grabar = ctk.CTkButton(
            button_frame,
            text="GRABAR",
            width=150,
            height=40,
            fg_color=self.color_blanco,
            text_color=self.color_negro,
            hover_color=self.color_gris,
            font=("Arial", 11, "bold"),
            border_width=2,
            border_color=self.color_rojo,
            command=self.grabar_datos
        )
        btn_grabar.pack(side="left", padx=10, expand=True)

        self.date_dropdown = DateDropdown(
            button_frame,
            values=self.generar_fechas(),
            command=self.on_date_selected,
            fg_color=self.color_blanco,
            width=120,
            height=28
        )
        self.date_dropdown.set(self.selected_date)
        self.date_dropdown.pack(side="right", padx=10)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ReporteDiarioApp()
    app.run()
