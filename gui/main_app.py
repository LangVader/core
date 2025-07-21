#!/usr/bin/env python3
"""
VADER GUI - Interfaz Gráfica Principal
Diseño: Moderno, Oscuro, Minimalista con Negro Predominante
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys
from pathlib import Path

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .editor import VaderEditor
from .ai_panel import VaderAIPanel
from .preview import VaderPreview

class VaderGUI:
    """Interfaz gráfica principal de Vader - Estilo oscuro y minimalista"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_theme()
        self.create_widgets()
        self.setup_layout()
        self.current_file = None
        
    def setup_window(self):
        """Configuración inicial de la ventana"""
        self.root.title("VADER - El Lenguaje Supremo Universal")
        self.root.geometry("1400x900")
        self.root.minsize(1000, 600)
        
        # Centrar ventana
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (900 // 2)
        self.root.geometry(f"1400x900+{x}+{y}")
        
        # Configurar cierre
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_theme(self):
        """Configurar tema oscuro y minimalista"""
        # Colores principales - Negro predominante
        self.colors = {
            'bg_primary': '#000000',      # Negro puro
            'bg_secondary': '#111111',    # Negro ligeramente más claro
            'bg_tertiary': '#1a1a1a',     # Gris muy oscuro
            'bg_accent': '#2d2d2d',       # Gris oscuro para elementos activos
            'fg_primary': '#ffffff',      # Blanco para texto principal
            'fg_secondary': '#cccccc',    # Gris claro para texto secundario
            'fg_accent': '#00ff41',       # Verde neón para acentos (estilo Matrix)
            'border': '#333333',          # Bordes sutiles
            'error': '#ff4444',           # Rojo para errores
            'warning': '#ffaa00',         # Naranja para advertencias
            'success': '#00ff41',         # Verde para éxito
            'button_hover': '#333333',    # Hover de botones
            'selection': '#0066cc'        # Azul para selecciones
        }
        
        # Configurar estilo de la ventana principal
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Configurar ttk style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configurar estilos personalizados
        self.configure_ttk_styles()
        
    def configure_ttk_styles(self):
        """Configurar estilos TTK personalizados"""
        # Frame principal
        self.style.configure('Dark.TFrame',
                           background=self.colors['bg_primary'],
                           borderwidth=0)
        
        # Frame secundario
        self.style.configure('DarkSecondary.TFrame',
                           background=self.colors['bg_secondary'],
                           borderwidth=1,
                           relief='solid')
        
        # Botones
        self.style.configure('Dark.TButton',
                           background=self.colors['bg_tertiary'],
                           foreground=self.colors['fg_primary'],
                           borderwidth=1,
                           focuscolor='none',
                           font=('Consolas', 10, 'bold'))
        
        self.style.map('Dark.TButton',
                      background=[('active', self.colors['button_hover']),
                                ('pressed', self.colors['bg_accent'])])
        
        # Labels
        self.style.configure('Dark.TLabel',
                           background=self.colors['bg_primary'],
                           foreground=self.colors['fg_primary'],
                           font=('Consolas', 10))
        
        # Notebook (pestañas)
        self.style.configure('Dark.TNotebook',
                           background=self.colors['bg_primary'],
                           borderwidth=0)
        
        self.style.configure('Dark.TNotebook.Tab',
                           background=self.colors['bg_tertiary'],
                           foreground=self.colors['fg_secondary'],
                           padding=[20, 8],
                           font=('Consolas', 9, 'bold'))
        
        self.style.map('Dark.TNotebook.Tab',
                      background=[('selected', self.colors['bg_secondary']),
                                ('active', self.colors['button_hover'])],
                      foreground=[('selected', self.colors['fg_accent'])])
        
    def create_widgets(self):
        """Crear todos los widgets de la interfaz"""
        try:
            print("🔧 Creando widgets...")
            
            # Frame principal
            self.main_frame = ttk.Frame(self.root, style='Dark.TFrame')
            print("✅ Frame principal creado")
            
            # Barra de menú superior
            self.create_menu_bar()
            print("✅ Barra de menú creada")
            
            # Barra de herramientas
            self.create_toolbar()
            print("✅ Barra de herramientas creada")
            
            # Panel principal con pestañas
            self.create_main_panel()
            print("✅ Panel principal creado")
            
            # Barra de estado
            self.create_status_bar()
            print("✅ Barra de estado creada")
            
        except Exception as e:
            print(f"❌ Error creando widgets: {e}")
            import traceback
            traceback.print_exc()
        
    def create_menu_bar(self):
        """Crear barra de menú minimalista"""
        self.menu_frame = ttk.Frame(self.main_frame, style='DarkSecondary.TFrame')
        
        # Logo y título
        title_label = ttk.Label(self.menu_frame, 
                               text="⚡ VADER", 
                               style='Dark.TLabel',
                               font=('Consolas', 16, 'bold'))
        title_label.configure(foreground=self.colors['fg_accent'])
        title_label.pack(side='left', padx=20, pady=10)
        
        # Subtítulo
        subtitle_label = ttk.Label(self.menu_frame,
                                 text="El Lenguaje Supremo Universal",
                                 style='Dark.TLabel',
                                 font=('Consolas', 9))
        subtitle_label.configure(foreground=self.colors['fg_secondary'])
        subtitle_label.pack(side='left', padx=(0, 20), pady=10)
        
        # Botones principales
        btn_frame = ttk.Frame(self.menu_frame, style='Dark.TFrame')
        btn_frame.pack(side='right', padx=20, pady=5)
        
        buttons = [
            ("📁 Abrir", self.open_file),
            ("💾 Guardar", self.save_file),
            ("▶️ Ejecutar", self.run_code),
            ("🤖 IA", self.toggle_ai_panel)
        ]
        
        for text, command in buttons:
            btn = ttk.Button(btn_frame, text=text, command=command, style='Dark.TButton')
            btn.pack(side='left', padx=5)
            
    def create_toolbar(self):
        """Crear barra de herramientas"""
        self.toolbar_frame = ttk.Frame(self.main_frame, style='Dark.TFrame')
        
        # Selector de lenguaje objetivo
        ttk.Label(self.toolbar_frame, text="Lenguaje:", style='Dark.TLabel').pack(side='left', padx=10)
        
        self.target_var = tk.StringVar(value="python")
        self.target_combo = ttk.Combobox(self.toolbar_frame, 
                                       textvariable=self.target_var,
                                       values=["python", "javascript", "java", "csharp", "go", "rust"],
                                       state="readonly",
                                       width=12)
        self.target_combo.pack(side='left', padx=5)
        
        # Selector de framework
        ttk.Label(self.toolbar_frame, text="Framework:", style='Dark.TLabel').pack(side='left', padx=(20, 10))
        
        self.framework_var = tk.StringVar()
        self.framework_combo = ttk.Combobox(self.toolbar_frame,
                                          textvariable=self.framework_var,
                                          values=["", "react", "vue", "angular", "nextjs", "express"],
                                          state="readonly",
                                          width=12)
        self.framework_combo.pack(side='left', padx=5)
        
    def create_main_panel(self):
        """Crear panel principal con pestañas"""
        # Notebook para pestañas
        self.notebook = ttk.Notebook(self.main_frame, style='Dark.TNotebook')
        
        # Pestaña del Editor
        self.editor_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(self.editor_frame, text="📝 Editor")
        
        # Crear editor de código
        self.editor = VaderEditor(self.editor_frame, self.colors)
        
        # Pestaña de Vista Previa
        self.preview_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(self.preview_frame, text="👁️ Vista Previa")
        
        # Crear vista previa
        self.preview = VaderPreview(self.preview_frame, self.colors)
        
        # Panel de IA (inicialmente oculto)
        self.ai_panel = VaderAIPanel(self.main_frame, self.colors)
        self.ai_visible = False
        
    def create_status_bar(self):
        """Crear barra de estado"""
        self.status_frame = ttk.Frame(self.main_frame, style='DarkSecondary.TFrame')
        
        # Información del archivo
        self.file_info_var = tk.StringVar(value="Sin archivo")
        file_label = ttk.Label(self.status_frame, 
                              textvariable=self.file_info_var,
                              style='Dark.TLabel')
        file_label.pack(side='left', padx=10, pady=5)
        
        # Estado de la IA
        self.ai_status_var = tk.StringVar(value="IA: Lista")
        ai_label = ttk.Label(self.status_frame,
                            textvariable=self.ai_status_var,
                            style='Dark.TLabel')
        ai_label.configure(foreground=self.colors['success'])
        ai_label.pack(side='right', padx=10, pady=5)
        
    def setup_layout(self):
        """Configurar el layout de la interfaz"""
        try:
            print("🔧 Configurando layout...")
            
            # Frame principal primero
            self.main_frame.pack(fill='both', expand=True)
            print("✅ Main frame packed")
            
            # Verificar que los widgets existen antes de hacer pack
            if hasattr(self, 'menu_frame'):
                self.menu_frame.pack(fill='x', pady=(0, 1))
                print("✅ Menu frame packed")
            
            if hasattr(self, 'toolbar_frame'):
                self.toolbar_frame.pack(fill='x', pady=1)
                print("✅ Toolbar frame packed")
            
            if hasattr(self, 'notebook'):
                self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
                print("✅ Notebook packed")
            
            if hasattr(self, 'status_frame'):
                self.status_frame.pack(fill='x', pady=(1, 0))
                print("✅ Status frame packed")
                
            # Forzar actualización
            self.root.update_idletasks()
            print("✅ Layout configurado exitosamente")
            
        except Exception as e:
            print(f"❌ Error configurando layout: {e}")
            import traceback
            traceback.print_exc()
        
    def toggle_ai_panel(self):
        """Mostrar/ocultar panel de IA"""
        if not self.ai_visible:
            # Mostrar panel de IA
            self.ai_panel.show()
            self.ai_visible = True
        else:
            # Ocultar panel de IA
            self.ai_panel.hide()
            self.ai_visible = False
            
    def open_file(self):
        """Abrir archivo .vdr"""
        file_path = filedialog.askopenfilename(
            title="Abrir archivo Vader",
            filetypes=[("Archivos Vader", "*.vdr"), ("Todos los archivos", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.editor.set_content(content)
                self.current_file = file_path
                self.file_info_var.set(f"Archivo: {os.path.basename(file_path)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}")
                
    def save_file(self):
        """Guardar archivo actual"""
        if not self.current_file:
            self.save_file_as()
            return
            
        try:
            content = self.editor.get_content()
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            messagebox.showinfo("Éxito", "Archivo guardado correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")
            
    def save_file_as(self):
        """Guardar archivo como"""
        file_path = filedialog.asksaveasfilename(
            title="Guardar archivo Vader",
            defaultextension=".vdr",
            filetypes=[("Archivos Vader", "*.vdr"), ("Todos los archivos", "*.*")]
        )
        
        if file_path:
            self.current_file = file_path
            self.save_file()
            self.file_info_var.set(f"Archivo: {os.path.basename(file_path)}")
            
    def run_code(self):
        """Ejecutar código Vader"""
        if not self.editor.get_content().strip():
            messagebox.showwarning("Advertencia", "No hay código para ejecutar")
            return
            
        # Cambiar a pestaña de vista previa
        self.notebook.select(self.preview_frame)
        
        # Ejecutar transpilación
        self.preview.transpile_and_show(
            self.editor.get_content(),
            self.target_var.get(),
            self.framework_var.get()
        )
        
    def on_closing(self):
        """Manejar cierre de la aplicación"""
        if messagebox.askokcancel("Salir", "¿Estás seguro de que quieres salir de Vader?"):
            self.root.destroy()
            
    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

def main():
    """Función principal para ejecutar la GUI"""
    app = VaderGUI()
    app.run()

if __name__ == "__main__":
    main()
