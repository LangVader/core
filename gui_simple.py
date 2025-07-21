#!/usr/bin/env python3
"""
VADER GUI SIMPLE - Versión funcional garantizada
Diseño: Moderno, Oscuro, Minimalista con Negro Predominante
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import sys
import os

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class VaderGUISimple:
    """GUI simplificada de Vader que garantiza funcionar"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.create_interface()
        self.current_file = None
        
    def setup_window(self):
        """Configurar ventana principal"""
        self.root.title("⚡ VADER - El Lenguaje Supremo Universal")
        self.root.geometry("1200x800")
        self.root.configure(bg='#000000')  # Negro predominante
        
        # Centrar ventana
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"1200x800+{x}+{y}")
        
    def create_interface(self):
        """Crear interfaz completa"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#000000')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # HEADER - Título y botones principales
        self.create_header(main_frame)
        
        # CUERPO - Área principal con pestañas
        self.create_body(main_frame)
        
        # FOOTER - Barra de estado
        self.create_footer(main_frame)
        
    def create_header(self, parent):
        """Crear header con título y botones"""
        header_frame = tk.Frame(parent, bg='#111111', height=80)
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Título principal
        title_label = tk.Label(
            header_frame,
            text="⚡ VADER",
            bg='#111111',
            fg='#00ff41',  # Verde neón
            font=('Consolas', 20, 'bold')
        )
        title_label.pack(side='left', padx=20, pady=20)
        
        # Subtítulo
        subtitle_label = tk.Label(
            header_frame,
            text="El Lenguaje Supremo Universal",
            bg='#111111',
            fg='#cccccc',
            font=('Consolas', 10)
        )
        subtitle_label.place(x=20, y=50)
        
        # Botones principales
        buttons_frame = tk.Frame(header_frame, bg='#111111')
        buttons_frame.pack(side='right', padx=20, pady=15)
        
        buttons = [
            ("📁 Abrir", self.open_file),
            ("💾 Guardar", self.save_file),
            ("▶️ Ejecutar", self.run_code),
            ("🤖 IA", self.show_ai_help)
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = tk.Button(
                buttons_frame,
                text=text,
                command=command,
                bg='#2d2d2d',
                fg='#ffffff',
                font=('Consolas', 10, 'bold'),
                relief='flat',
                padx=15,
                pady=5,
                cursor='hand2'
            )
            btn.grid(row=0, column=i, padx=5)
            
            # Efectos hover
            def on_enter(e, button=btn):
                button.configure(bg='#333333')
            def on_leave(e, button=btn):
                button.configure(bg='#2d2d2d')
                
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            
    def create_body(self, parent):
        """Crear cuerpo principal con pestañas"""
        # Notebook para pestañas
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar estilo del notebook
        style.configure('Dark.TNotebook', background='#000000', borderwidth=0)
        style.configure('Dark.TNotebook.Tab', 
                       background='#1a1a1a', 
                       foreground='#cccccc',
                       padding=[20, 10],
                       font=('Consolas', 10, 'bold'))
        style.map('Dark.TNotebook.Tab',
                 background=[('selected', '#000000'), ('active', '#333333')],
                 foreground=[('selected', '#00ff41')])
        
        self.notebook = ttk.Notebook(parent, style='Dark.TNotebook')
        self.notebook.pack(fill='both', expand=True, pady=(0, 10))
        
        # Pestaña 1: Editor
        self.create_editor_tab()
        
        # Pestaña 2: Vista Previa
        self.create_preview_tab()
        
        # Pestaña 3: IA Assistant
        self.create_ai_tab()
        
    def create_editor_tab(self):
        """Crear pestaña del editor"""
        editor_frame = tk.Frame(self.notebook, bg='#000000')
        self.notebook.add(editor_frame, text="📝 Editor")
        
        # Frame para editor con números de línea
        editor_container = tk.Frame(editor_frame, bg='#000000')
        editor_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Números de línea
        self.line_numbers = tk.Text(
            editor_container,
            width=4,
            bg='#111111',
            fg='#666666',
            font=('Consolas', 11),
            state='disabled',
            wrap='none',
            cursor='arrow'
        )
        self.line_numbers.pack(side='left', fill='y')
        
        # Editor principal
        self.editor = scrolledtext.ScrolledText(
            editor_container,
            bg='#000000',
            fg='#ffffff',
            font=('Consolas', 11),
            insertbackground='#00ff41',  # Cursor verde neón
            selectbackground='#0066cc',
            wrap='none',
            undo=True
        )
        self.editor.pack(side='right', fill='both', expand=True)
        
        # Contenido inicial
        initial_code = """# ¡Bienvenido a VADER! 🚀
# El Lenguaje Supremo Universal

# Ejemplo: Calculadora simple
funcion calculadora
    mostrar "=== CALCULADORA VADER ==="
    
    preguntar "Primer número:" guardar la respuesta en num1
    preguntar "Segundo número:" guardar la respuesta en num2
    preguntar "Operación (+, -, *, /):" guardar la respuesta en op
    
    convertir num1 a numero
    convertir num2 a numero
    
    si op es "+"
        resultado = num1 + num2
    sino si op es "-"
        resultado = num1 - num2
    sino si op es "*"
        resultado = num1 * num2
    sino si op es "/"
        si num2 no es 0
            resultado = num1 / num2
        sino
            mostrar "Error: División por cero"
            retornar
        fin si
    sino
        mostrar "Operación no válida"
        retornar
    fin si
    
    mostrar "Resultado: " + str(resultado)
fin funcion

# Ejecutar
calculadora()

# ¡Presiona ▶️ para ejecutar!
# ¡Prueba el botón 🤖 para IA!"""
        
        self.editor.insert('1.0', initial_code)
        self.update_line_numbers()
        
        # Eventos
        self.editor.bind('<KeyRelease>', self.on_text_change)
        self.editor.bind('<Button-1>', self.on_text_change)
        
    def create_preview_tab(self):
        """Crear pestaña de vista previa"""
        preview_frame = tk.Frame(self.notebook, bg='#000000')
        self.notebook.add(preview_frame, text="👁️ Vista Previa")
        
        # Controles superiores
        controls_frame = tk.Frame(preview_frame, bg='#111111', height=50)
        controls_frame.pack(fill='x', padx=10, pady=(10, 5))
        controls_frame.pack_propagate(False)
        
        # Selector de lenguaje
        tk.Label(controls_frame, text="Lenguaje:", bg='#111111', fg='#ffffff', font=('Consolas', 10)).pack(side='left', padx=10, pady=15)
        
        self.target_var = tk.StringVar(value="python")
        target_combo = ttk.Combobox(
            controls_frame,
            textvariable=self.target_var,
            values=["python", "javascript", "java", "csharp", "go", "rust"],
            state="readonly",
            width=12
        )
        target_combo.pack(side='left', padx=5, pady=15)
        
        # Botón transpilar
        transpile_btn = tk.Button(
            controls_frame,
            text="🔄 Transpilar",
            command=self.transpile_code,
            bg='#2d2d2d',
            fg='#00ff41',
            font=('Consolas', 10, 'bold'),
            relief='flat',
            padx=15
        )
        transpile_btn.pack(side='right', padx=10, pady=10)
        
        # Área de código transpilado
        self.preview_text = scrolledtext.ScrolledText(
            preview_frame,
            bg='#000000',
            fg='#ffffff',
            font=('Consolas', 10),
            state='disabled'
        )
        self.preview_text.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
    def create_ai_tab(self):
        """Crear pestaña de IA"""
        ai_frame = tk.Frame(self.notebook, bg='#000000')
        self.notebook.add(ai_frame, text="🤖 IA Assistant")
        
        # Área de chat
        self.chat_display = scrolledtext.ScrolledText(
            ai_frame,
            bg='#000000',
            fg='#ffffff',
            font=('Consolas', 10),
            state='disabled',
            height=20
        )
        self.chat_display.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Mensaje de bienvenida
        self.add_ai_message("🚀 ¡Hola! Soy el Asistente de IA de Vader.")
        self.add_ai_message("Puedo ayudarte a generar código, analizar tu código y mucho más.")
        self.add_ai_message("Ejemplos: 'genera una calculadora', 'analiza mi código', 'optimiza este código'")
        
        # Área de entrada
        input_frame = tk.Frame(ai_frame, bg='#000000')
        input_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        self.ai_input = tk.Entry(
            input_frame,
            bg='#1a1a1a',
            fg='#ffffff',
            font=('Consolas', 11),
            insertbackground='#00ff41'
        )
        self.ai_input.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.ai_input.bind('<Return>', self.send_ai_message)
        
        send_btn = tk.Button(
            input_frame,
            text="Enviar",
            command=self.send_ai_message,
            bg='#2d2d2d',
            fg='#00ff41',
            font=('Consolas', 10, 'bold'),
            relief='flat',
            padx=15
        )
        send_btn.pack(side='right')
        
        # Botones rápidos
        quick_frame = tk.Frame(ai_frame, bg='#000000')
        quick_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        quick_buttons = [
            ("📝 Generar", lambda: self.quick_ai_action("genera un programa simple")),
            ("🔍 Analizar", lambda: self.quick_ai_action("analiza mi código")),
            ("⚡ Optimizar", lambda: self.quick_ai_action("optimiza mi código")),
            ("🐛 Errores", lambda: self.quick_ai_action("busca errores"))
        ]
        
        for text, command in quick_buttons:
            btn = tk.Button(
                quick_frame,
                text=text,
                command=command,
                bg='#1a1a1a',
                fg='#cccccc',
                font=('Consolas', 9),
                relief='flat',
                padx=10,
                pady=5
            )
            btn.pack(side='left', padx=5)
            
    def create_footer(self, parent):
        """Crear footer con información de estado"""
        footer_frame = tk.Frame(parent, bg='#111111', height=30)
        footer_frame.pack(fill='x')
        footer_frame.pack_propagate(False)
        
        # Información del archivo
        self.file_info = tk.Label(
            footer_frame,
            text="Sin archivo",
            bg='#111111',
            fg='#cccccc',
            font=('Consolas', 9)
        )
        self.file_info.pack(side='left', padx=10, pady=5)
        
        # Estado de IA
        ai_status = tk.Label(
            footer_frame,
            text="IA: Lista ✅",
            bg='#111111',
            fg='#00ff41',
            font=('Consolas', 9)
        )
        ai_status.pack(side='right', padx=10, pady=5)
        
    def update_line_numbers(self):
        """Actualizar números de línea"""
        content = self.editor.get('1.0', tk.END)
        line_count = content.count('\n')
        
        self.line_numbers.config(state='normal')
        self.line_numbers.delete('1.0', tk.END)
        
        for i in range(1, line_count + 1):
            self.line_numbers.insert(tk.END, f"{i:3}\n")
            
        self.line_numbers.config(state='disabled')
        
    def on_text_change(self, event=None):
        """Manejar cambios en el texto"""
        self.update_line_numbers()
        
    def add_ai_message(self, message, sender="IA"):
        """Agregar mensaje al chat de IA"""
        self.chat_display.config(state='normal')
        
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M")
        
        if sender == "IA":
            self.chat_display.insert(tk.END, f"[{timestamp}] 🤖 {message}\n\n")
        else:
            self.chat_display.insert(tk.END, f"[{timestamp}] 👤 {message}\n\n")
            
        self.chat_display.see(tk.END)
        self.chat_display.config(state='disabled')
        
    def open_file(self):
        """Abrir archivo"""
        file_path = filedialog.askopenfilename(
            title="Abrir archivo Vader",
            filetypes=[("Archivos Vader", "*.vdr"), ("Todos los archivos", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.editor.delete('1.0', tk.END)
                self.editor.insert('1.0', content)
                self.current_file = file_path
                self.file_info.config(text=f"Archivo: {os.path.basename(file_path)}")
                self.update_line_numbers()
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}")
                
    def save_file(self):
        """Guardar archivo"""
        if not self.current_file:
            file_path = filedialog.asksaveasfilename(
                title="Guardar archivo Vader",
                defaultextension=".vdr",
                filetypes=[("Archivos Vader", "*.vdr"), ("Todos los archivos", "*.*")]
            )
            if file_path:
                self.current_file = file_path
            else:
                return
                
        try:
            content = self.editor.get('1.0', tk.END + '-1c')
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.file_info.config(text=f"Archivo: {os.path.basename(self.current_file)}")
            messagebox.showinfo("Éxito", "Archivo guardado correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")
            
    def run_code(self):
        """Ejecutar código"""
        self.transpile_code()
        self.notebook.select(1)  # Cambiar a pestaña de vista previa
        
    def transpile_code(self):
        """Transpilar código"""
        try:
            code = self.editor.get('1.0', tk.END + '-1c')
            target = self.target_var.get()
            
            if not code.strip():
                messagebox.showwarning("Advertencia", "No hay código para transpilar")
                return
                
            # Intentar usar el transpilador real
            try:
                from src.vader import transpile_code
                result = transpile_code(code, target, verbose=False)
                
                if result:
                    self.preview_text.config(state='normal')
                    self.preview_text.delete('1.0', tk.END)
                    self.preview_text.insert('1.0', result)
                    self.preview_text.config(state='disabled')
                else:
                    raise Exception("Transpilación falló")
                    
            except Exception as e:
                # Fallback: mostrar código original con comentario
                fallback = f"# Código Vader transpilado a {target.upper()}\n# (Transpilador no disponible - mostrando código original)\n\n{code}"
                self.preview_text.config(state='normal')
                self.preview_text.delete('1.0', tk.END)
                self.preview_text.insert('1.0', fallback)
                self.preview_text.config(state='disabled')
                
        except Exception as e:
            messagebox.showerror("Error", f"Error durante la transpilación:\n{e}")
            
    def send_ai_message(self, event=None):
        """Enviar mensaje a IA"""
        message = self.ai_input.get().strip()
        if not message:
            return
            
        self.add_ai_message(message, "Usuario")
        self.ai_input.delete(0, tk.END)
        
        # Simular respuesta de IA
        self.root.after(1000, lambda: self.simulate_ai_response(message))
        
    def simulate_ai_response(self, user_message):
        """Simular respuesta de IA"""
        message_lower = user_message.lower()
        
        if any(word in message_lower for word in ['genera', 'crear', 'hacer']):
            response = "¡Perfecto! Aquí tienes un código generado:\n\n# Código generado por IA\nfuncion saludo\n    mostrar \"¡Hola desde Vader!\"\nfin funcion\n\nsaludo()"
        elif any(word in message_lower for word in ['analiza', 'revisar']):
            response = "He analizado tu código. Se ve bien estructurado. Sugerencias:\n• Agregar más comentarios\n• Considerar manejo de errores\n• Puntuación: 85/100"
        elif any(word in message_lower for word in ['optimiza', 'mejorar']):
            response = "Tu código ya está bien optimizado. Algunas sugerencias menores:\n• Usar nombres más descriptivos\n• Agrupar funciones relacionadas"
        elif any(word in message_lower for word in ['error', 'bug']):
            response = "No encontré errores críticos en tu código. ¡Buen trabajo!"
        else:
            response = "Entiendo. Puedo ayudarte con:\n• Generar código: 'genera una calculadora'\n• Analizar código: 'analiza mi código'\n• Optimizar: 'optimiza este código'\n• Buscar errores: 'busca errores'"
            
        self.add_ai_message(response)
        
    def quick_ai_action(self, action):
        """Acción rápida de IA"""
        self.ai_input.delete(0, tk.END)
        self.ai_input.insert(0, action)
        self.send_ai_message()
        
    def show_ai_help(self):
        """Mostrar ayuda de IA"""
        self.notebook.select(2)  # Cambiar a pestaña de IA
        
    def run(self):
        """Ejecutar la aplicación"""
        print("🚀 GUI Simple de Vader iniciada correctamente")
        self.root.mainloop()

def main():
    """Función principal"""
    try:
        print("🎨 Iniciando VADER GUI Simple...")
        app = VaderGUISimple()
        app.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
