#!/usr/bin/env python3
"""
VADER PREVIEW - Vista Previa de Código Transpilado
Diseño: Moderno, Oscuro, Minimalista con Negro Predominante
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
import os
import subprocess
import tempfile

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class VaderPreview:
    """Vista previa del código transpilado y resultados de ejecución"""
    
    def __init__(self, parent, colors):
        self.parent = parent
        self.colors = colors
        self.setup_preview()
        
    def setup_preview(self):
        """Configurar vista previa"""
        # Frame principal
        self.preview_frame = tk.Frame(self.parent, bg=self.colors['bg_primary'])
        self.preview_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Notebook para pestañas de vista previa
        self.preview_notebook = ttk.Notebook(self.preview_frame, style='Dark.TNotebook')
        self.preview_notebook.pack(fill='both', expand=True)
        
        # Pestaña de código transpilado
        self.create_transpiled_tab()
        
        # Pestaña de salida de ejecución
        self.create_output_tab()
        
        # Pestaña de métricas
        self.create_metrics_tab()
        
        # Panel de control
        self.create_control_panel()
        
    def create_transpiled_tab(self):
        """Crear pestaña de código transpilado"""
        self.transpiled_frame = ttk.Frame(self.preview_notebook, style='Dark.TFrame')
        self.preview_notebook.add(self.transpiled_frame, text="📄 Código Transpilado")
        
        # Header
        header_frame = ttk.Frame(self.transpiled_frame, style='Dark.TFrame')
        header_frame.pack(fill='x', padx=10, pady=(10, 5))
        
        self.transpiled_info = ttk.Label(header_frame,
                                       text="Lenguaje: No transpilado",
                                       style='Dark.TLabel',
                                       font=('Consolas', 10))
        self.transpiled_info.pack(side='left')
        
        # Botón copiar
        copy_btn = ttk.Button(header_frame,
                             text="📋 Copiar",
                             command=self.copy_transpiled,
                             style='Dark.TButton')
        copy_btn.pack(side='right')
        
        # Área de código transpilado
        self.transpiled_text = scrolledtext.ScrolledText(
            self.transpiled_frame,
            wrap='none',
            bg=self.colors['bg_primary'],
            fg=self.colors['fg_primary'],
            font=('Consolas', 10),
            insertbackground=self.colors['fg_accent'],
            selectbackground=self.colors['selection'],
            borderwidth=1,
            relief='solid',
            state='disabled'
        )
        self.transpiled_text.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Configurar syntax highlighting básico
        self.transpiled_text.tag_configure('keyword', foreground=self.colors['fg_accent'], font=('Consolas', 10, 'bold'))
        self.transpiled_text.tag_configure('string', foreground='#ffa500')
        self.transpiled_text.tag_configure('comment', foreground=self.colors['fg_secondary'])
        
    def create_output_tab(self):
        """Crear pestaña de salida de ejecución"""
        self.output_frame = ttk.Frame(self.preview_notebook, style='Dark.TFrame')
        self.preview_notebook.add(self.output_frame, text="▶️ Salida")
        
        # Header
        header_frame = ttk.Frame(self.output_frame, style='Dark.TFrame')
        header_frame.pack(fill='x', padx=10, pady=(10, 5))
        
        self.execution_status = ttk.Label(header_frame,
                                        text="Estado: Listo para ejecutar",
                                        style='Dark.TLabel',
                                        font=('Consolas', 10))
        self.execution_status.pack(side='left')
        
        # Botón limpiar salida
        clear_btn = ttk.Button(header_frame,
                              text="🗑️ Limpiar",
                              command=self.clear_output,
                              style='Dark.TButton')
        clear_btn.pack(side='right')
        
        # Área de salida
        self.output_text = scrolledtext.ScrolledText(
            self.output_frame,
            wrap='word',
            bg=self.colors['bg_primary'],
            fg=self.colors['fg_primary'],
            font=('Consolas', 10),
            insertbackground=self.colors['fg_accent'],
            selectbackground=self.colors['selection'],
            borderwidth=1,
            relief='solid',
            state='disabled'
        )
        self.output_text.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Tags para diferentes tipos de salida
        self.output_text.tag_configure('stdout', foreground=self.colors['fg_primary'])
        self.output_text.tag_configure('stderr', foreground=self.colors['error'])
        self.output_text.tag_configure('success', foreground=self.colors['success'])
        self.output_text.tag_configure('info', foreground=self.colors['fg_accent'])
        
    def create_metrics_tab(self):
        """Crear pestaña de métricas"""
        self.metrics_frame = ttk.Frame(self.preview_notebook, style='Dark.TFrame')
        self.preview_notebook.add(self.metrics_frame, text="📊 Métricas")
        
        # Crear área de métricas con scroll
        metrics_canvas = tk.Canvas(self.metrics_frame, bg=self.colors['bg_primary'])
        metrics_scrollbar = ttk.Scrollbar(self.metrics_frame, orient="vertical", command=metrics_canvas.yview)
        self.metrics_content = ttk.Frame(metrics_canvas, style='Dark.TFrame')
        
        self.metrics_content.bind(
            "<Configure>",
            lambda e: metrics_canvas.configure(scrollregion=metrics_canvas.bbox("all"))
        )
        
        metrics_canvas.create_window((0, 0), window=self.metrics_content, anchor="nw")
        metrics_canvas.configure(yscrollcommand=metrics_scrollbar.set)
        
        metrics_canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        metrics_scrollbar.pack(side="right", fill="y", pady=10)
        
        # Inicializar métricas vacías
        self.show_empty_metrics()
        
    def create_control_panel(self):
        """Crear panel de control"""
        control_frame = ttk.Frame(self.preview_frame, style='DarkSecondary.TFrame')
        control_frame.pack(fill='x', pady=(10, 0))
        
        # Botones de control
        ttk.Button(control_frame,
                  text="🔄 Transpilar",
                  command=self.manual_transpile,
                  style='Dark.TButton').pack(side='left', padx=10, pady=10)
        
        ttk.Button(control_frame,
                  text="▶️ Ejecutar",
                  command=self.execute_code,
                  style='Dark.TButton').pack(side='left', padx=5, pady=10)
        
        ttk.Button(control_frame,
                  text="💾 Guardar",
                  command=self.save_transpiled,
                  style='Dark.TButton').pack(side='left', padx=5, pady=10)
        
        # Información de estado
        self.status_var = tk.StringVar(value="Listo")
        status_label = ttk.Label(control_frame,
                               textvariable=self.status_var,
                               style='Dark.TLabel')
        status_label.pack(side='right', padx=10, pady=10)
        
    def transpile_and_show(self, code, target_lang, framework=None):
        """Transpilar código y mostrar resultado"""
        try:
            self.status_var.set("Transpilando...")
            self.parent.update()
            
            # Importar el sistema de transpilación
            from src.vader import transpile_code
            
            # Transpilar código
            result = transpile_code(code, target_lang, framework=framework, verbose=False)
            
            if result:
                # Mostrar código transpilado
                self.show_transpiled_code(result, target_lang, framework)
                
                # Actualizar métricas
                self.update_metrics(code, result, target_lang)
                
                # Cambiar a pestaña de código transpilado
                self.preview_notebook.select(0)
                
                self.status_var.set("Transpilación exitosa")
                self.add_output("✅ Transpilación completada exitosamente", 'success')
                
            else:
                self.status_var.set("Error en transpilación")
                self.add_output("❌ Error durante la transpilación", 'stderr')
                
        except Exception as e:
            self.status_var.set("Error")
            self.add_output(f"❌ Error: {str(e)}", 'stderr')
            messagebox.showerror("Error", f"Error durante la transpilación:\n{e}")
            
    def show_transpiled_code(self, code, target_lang, framework=None):
        """Mostrar código transpilado"""
        self.transpiled_text.config(state='normal')
        self.transpiled_text.delete('1.0', tk.END)
        self.transpiled_text.insert('1.0', code)
        self.transpiled_text.config(state='disabled')
        
        # Actualizar información
        info_text = f"Lenguaje: {target_lang.upper()}"
        if framework:
            info_text += f" | Framework: {framework}"
        info_text += f" | Líneas: {len(code.splitlines())}"
        
        self.transpiled_info.config(text=info_text)
        
    def update_metrics(self, original_code, transpiled_code, target_lang):
        """Actualizar métricas de transpilación"""
        # Limpiar métricas anteriores
        for widget in self.metrics_content.winfo_children():
            widget.destroy()
            
        # Calcular métricas
        original_lines = len(original_code.splitlines())
        transpiled_lines = len(transpiled_code.splitlines())
        original_chars = len(original_code)
        transpiled_chars = len(transpiled_code)
        
        # Mostrar métricas
        metrics_data = [
            ("📝 Código Original", ""),
            ("  Líneas", str(original_lines)),
            ("  Caracteres", str(original_chars)),
            ("  Palabras", str(len(original_code.split()))),
            ("", ""),
            ("🔄 Código Transpilado", ""),
            ("  Lenguaje", target_lang.upper()),
            ("  Líneas", str(transpiled_lines)),
            ("  Caracteres", str(transpiled_chars)),
            ("  Palabras", str(len(transpiled_code.split()))),
            ("", ""),
            ("📊 Estadísticas", ""),
            ("  Ratio líneas", f"{transpiled_lines/original_lines:.2f}x" if original_lines > 0 else "N/A"),
            ("  Ratio caracteres", f"{transpiled_chars/original_chars:.2f}x" if original_chars > 0 else "N/A"),
            ("  Compresión", f"{((original_chars-transpiled_chars)/original_chars*100):.1f}%" if original_chars > 0 else "N/A"),
        ]
        
        for i, (label, value) in enumerate(metrics_data):
            if label == "":
                # Espaciador
                ttk.Label(self.metrics_content, text="", style='Dark.TLabel').grid(row=i, column=0, sticky='w', pady=2)
            elif label.startswith(("📝", "🔄", "📊")):
                # Título de sección
                title_label = ttk.Label(self.metrics_content, text=label, style='Dark.TLabel', font=('Consolas', 11, 'bold'))
                title_label.configure(foreground=self.colors['fg_accent'])
                title_label.grid(row=i, column=0, columnspan=2, sticky='w', pady=(10, 2))
            else:
                # Métrica normal
                ttk.Label(self.metrics_content, text=label, style='Dark.TLabel').grid(row=i, column=0, sticky='w', padx=(20, 10))
                value_label = ttk.Label(self.metrics_content, text=value, style='Dark.TLabel', font=('Consolas', 10, 'bold'))
                value_label.configure(foreground=self.colors['fg_secondary'])
                value_label.grid(row=i, column=1, sticky='w')
                
    def show_empty_metrics(self):
        """Mostrar métricas vacías"""
        empty_label = ttk.Label(self.metrics_content,
                              text="📊 Transpila código para ver métricas",
                              style='Dark.TLabel',
                              font=('Consolas', 12))
        empty_label.configure(foreground=self.colors['fg_secondary'])
        empty_label.pack(expand=True)
        
    def add_output(self, text, tag='stdout'):
        """Agregar texto a la salida"""
        self.output_text.config(state='normal')
        
        # Agregar timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        self.output_text.insert(tk.END, f"[{timestamp}] {text}\n", tag)
        self.output_text.see(tk.END)
        self.output_text.config(state='disabled')
        
        # Cambiar a pestaña de salida si hay error
        if tag == 'stderr':
            self.preview_notebook.select(1)
            
    def execute_code(self):
        """Ejecutar código transpilado"""
        try:
            transpiled_code = self.transpiled_text.get('1.0', tk.END).strip()
            if not transpiled_code:
                self.add_output("❌ No hay código transpilado para ejecutar", 'stderr')
                return
                
            self.execution_status.config(text="Estado: Ejecutando...")
            self.add_output("🚀 Iniciando ejecución...", 'info')
            
            # Determinar lenguaje por extensión
            lang_info = self.transpiled_info.cget('text')
            if 'python' in lang_info.lower():
                self.execute_python(transpiled_code)
            elif 'javascript' in lang_info.lower():
                self.execute_javascript(transpiled_code)
            else:
                self.add_output("❌ Ejecución no soportada para este lenguaje", 'stderr')
                
        except Exception as e:
            self.add_output(f"❌ Error durante la ejecución: {str(e)}", 'stderr')
            self.execution_status.config(text="Estado: Error")
            
    def execute_python(self, code):
        """Ejecutar código Python"""
        try:
            # Crear archivo temporal
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
                
            # Ejecutar
            result = subprocess.run(
                ['python3', temp_file],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Mostrar resultados
            if result.stdout:
                self.add_output("📤 SALIDA:", 'info')
                self.add_output(result.stdout, 'stdout')
                
            if result.stderr:
                self.add_output("⚠️ ERRORES:", 'info')
                self.add_output(result.stderr, 'stderr')
                
            if result.returncode == 0:
                self.add_output("✅ Ejecución completada exitosamente", 'success')
                self.execution_status.config(text="Estado: Ejecutado exitosamente")
            else:
                self.add_output(f"❌ Código de salida: {result.returncode}", 'stderr')
                self.execution_status.config(text="Estado: Error en ejecución")
                
            # Limpiar archivo temporal
            os.unlink(temp_file)
            
        except subprocess.TimeoutExpired:
            self.add_output("⏰ Tiempo de ejecución agotado (10s)", 'stderr')
            self.execution_status.config(text="Estado: Timeout")
        except Exception as e:
            self.add_output(f"❌ Error: {str(e)}", 'stderr')
            self.execution_status.config(text="Estado: Error")
            
    def execute_javascript(self, code):
        """Ejecutar código JavaScript"""
        try:
            # Crear archivo temporal
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                f.write(code)
                temp_file = f.name
                
            # Intentar ejecutar con node
            result = subprocess.run(
                ['node', temp_file],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Mostrar resultados
            if result.stdout:
                self.add_output("📤 SALIDA:", 'info')
                self.add_output(result.stdout, 'stdout')
                
            if result.stderr:
                self.add_output("⚠️ ERRORES:", 'info')
                self.add_output(result.stderr, 'stderr')
                
            if result.returncode == 0:
                self.add_output("✅ Ejecución completada exitosamente", 'success')
                self.execution_status.config(text="Estado: Ejecutado exitosamente")
            else:
                self.add_output(f"❌ Código de salida: {result.returncode}", 'stderr')
                self.execution_status.config(text="Estado: Error en ejecución")
                
            # Limpiar archivo temporal
            os.unlink(temp_file)
            
        except FileNotFoundError:
            self.add_output("❌ Node.js no encontrado. Instala Node.js para ejecutar JavaScript.", 'stderr')
            self.execution_status.config(text="Estado: Node.js no disponible")
        except subprocess.TimeoutExpired:
            self.add_output("⏰ Tiempo de ejecución agotado (10s)", 'stderr')
            self.execution_status.config(text="Estado: Timeout")
        except Exception as e:
            self.add_output(f"❌ Error: {str(e)}", 'stderr')
            self.execution_status.config(text="Estado: Error")
            
    def manual_transpile(self):
        """Transpilación manual desde el editor"""
        try:
            # Obtener código del editor principal
            root = self.parent
            while root.master:
                root = root.master
                
            # Buscar el editor y configuración
            editor_content = ""
            target_lang = "python"
            framework = None
            
            for widget in root.winfo_children():
                if hasattr(widget, 'editor'):
                    editor_content = widget.editor.get_content()
                if hasattr(widget, 'target_var'):
                    target_lang = widget.target_var.get()
                if hasattr(widget, 'framework_var'):
                    framework = widget.framework_var.get() or None
                    
            if editor_content.strip():
                self.transpile_and_show(editor_content, target_lang, framework)
            else:
                self.add_output("❌ No hay código en el editor para transpilar", 'stderr')
                
        except Exception as e:
            self.add_output(f"❌ Error: {str(e)}", 'stderr')
            
    def copy_transpiled(self):
        """Copiar código transpilado al portapapeles"""
        try:
            code = self.transpiled_text.get('1.0', tk.END).strip()
            if code:
                self.parent.clipboard_clear()
                self.parent.clipboard_append(code)
                self.add_output("📋 Código copiado al portapapeles", 'success')
            else:
                self.add_output("❌ No hay código para copiar", 'stderr')
        except Exception as e:
            self.add_output(f"❌ Error al copiar: {str(e)}", 'stderr')
            
    def save_transpiled(self):
        """Guardar código transpilado"""
        try:
            from tkinter import filedialog
            
            code = self.transpiled_text.get('1.0', tk.END).strip()
            if not code:
                self.add_output("❌ No hay código para guardar", 'stderr')
                return
                
            # Determinar extensión
            lang_info = self.transpiled_info.cget('text').lower()
            if 'python' in lang_info:
                ext = '.py'
            elif 'javascript' in lang_info:
                ext = '.js'
            elif 'java' in lang_info:
                ext = '.java'
            else:
                ext = '.txt'
                
            file_path = filedialog.asksaveasfilename(
                title="Guardar código transpilado",
                defaultextension=ext,
                filetypes=[("Archivo de código", f"*{ext}"), ("Todos los archivos", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(code)
                self.add_output(f"💾 Código guardado en: {file_path}", 'success')
                
        except Exception as e:
            self.add_output(f"❌ Error al guardar: {str(e)}", 'stderr')
            
    def clear_output(self):
        """Limpiar salida"""
        self.output_text.config(state='normal')
        self.output_text.delete('1.0', tk.END)
        self.output_text.config(state='disabled')
        self.execution_status.config(text="Estado: Listo para ejecutar")
