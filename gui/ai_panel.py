#!/usr/bin/env python3
"""
VADER AI PANEL - Panel de Inteligencia Artificial
Diseño: Moderno, Oscuro, Minimalista con Negro Predominante
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
import os

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class VaderAIPanel:
    """Panel de IA integrada para Vader"""
    
    def __init__(self, parent, colors):
        self.parent = parent
        self.colors = colors
        self.visible = False
        self.setup_panel()
        
    def setup_panel(self):
        """Configurar panel de IA"""
        # Frame principal del panel (inicialmente oculto)
        self.ai_frame = ttk.Frame(self.parent, style='DarkSecondary.TFrame')
        
        # Header del panel
        self.create_header()
        
        # Área de chat con IA
        self.create_chat_area()
        
        # Área de entrada
        self.create_input_area()
        
        # Botones de acción rápida
        self.create_quick_actions()
        
    def create_header(self):
        """Crear header del panel de IA"""
        header_frame = ttk.Frame(self.ai_frame, style='Dark.TFrame')
        header_frame.pack(fill='x', padx=10, pady=(10, 5))
        
        # Título
        title_label = ttk.Label(header_frame, 
                               text="🤖 VADER AI ASSISTANT",
                               style='Dark.TLabel',
                               font=('Consolas', 12, 'bold'))
        title_label.configure(foreground=self.colors['fg_accent'])
        title_label.pack(side='left')
        
        # Estado
        self.status_label = ttk.Label(header_frame,
                                    text="● ONLINE",
                                    style='Dark.TLabel',
                                    font=('Consolas', 9))
        self.status_label.configure(foreground=self.colors['success'])
        self.status_label.pack(side='right')
        
        # Botón cerrar
        close_btn = ttk.Button(header_frame,
                              text="✕",
                              command=self.hide,
                              style='Dark.TButton',
                              width=3)
        close_btn.pack(side='right', padx=(10, 0))
        
    def create_chat_area(self):
        """Crear área de chat"""
        chat_frame = ttk.Frame(self.ai_frame, style='Dark.TFrame')
        chat_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Área de mensajes
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            height=15,
            wrap='word',
            bg=self.colors['bg_primary'],
            fg=self.colors['fg_primary'],
            font=('Consolas', 10),
            insertbackground=self.colors['fg_accent'],
            selectbackground=self.colors['selection'],
            borderwidth=1,
            relief='solid'
        )
        self.chat_display.pack(fill='both', expand=True)
        
        # Configurar tags para diferentes tipos de mensajes
        self.chat_display.tag_configure('user', foreground=self.colors['fg_accent'], font=('Consolas', 10, 'bold'))
        self.chat_display.tag_configure('ai', foreground=self.colors['fg_primary'])
        self.chat_display.tag_configure('system', foreground=self.colors['fg_secondary'], font=('Consolas', 9, 'italic'))
        self.chat_display.tag_configure('code', background=self.colors['bg_tertiary'], font=('Consolas', 9))
        self.chat_display.tag_configure('error', foreground=self.colors['error'])
        self.chat_display.tag_configure('success', foreground=self.colors['success'])
        
        # Mensaje de bienvenida
        self.add_system_message("🚀 ¡Bienvenido al Asistente de IA de Vader!")
        self.add_system_message("Puedes pedirme que genere código, analice tu código o te ayude con cualquier cosa.")
        self.add_system_message("Ejemplos: 'genera una calculadora', 'analiza mi código', 'optimiza este código'")
        
    def create_input_area(self):
        """Crear área de entrada"""
        input_frame = ttk.Frame(self.ai_frame, style='Dark.TFrame')
        input_frame.pack(fill='x', padx=10, pady=5)
        
        # Campo de entrada
        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(
            input_frame,
            textvariable=self.input_var,
            bg=self.colors['bg_tertiary'],
            fg=self.colors['fg_primary'],
            font=('Consolas', 10),
            insertbackground=self.colors['fg_accent'],
            borderwidth=1,
            relief='solid'
        )
        self.input_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        self.input_entry.bind('<Return>', self.send_message)
        
        # Botón enviar
        send_btn = ttk.Button(input_frame,
                             text="Enviar",
                             command=self.send_message,
                             style='Dark.TButton')
        send_btn.pack(side='right')
        
    def create_quick_actions(self):
        """Crear botones de acción rápida"""
        actions_frame = ttk.Frame(self.ai_frame, style='Dark.TFrame')
        actions_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        # Título
        ttk.Label(actions_frame, 
                 text="Acciones Rápidas:",
                 style='Dark.TLabel',
                 font=('Consolas', 9)).pack(anchor='w', pady=(0, 5))
        
        # Botones
        buttons_frame = ttk.Frame(actions_frame, style='Dark.TFrame')
        buttons_frame.pack(fill='x')
        
        quick_actions = [
            ("📝 Generar Código", self.quick_generate),
            ("🔍 Analizar", self.quick_analyze),
            ("⚡ Optimizar", self.quick_optimize),
            ("🐛 Buscar Errores", self.quick_check_errors)
        ]
        
        for i, (text, command) in enumerate(quick_actions):
            btn = ttk.Button(buttons_frame,
                           text=text,
                           command=command,
                           style='Dark.TButton',
                           width=15)
            btn.grid(row=i//2, column=i%2, padx=2, pady=2, sticky='ew')
            
        # Configurar grid
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
        
    def show(self):
        """Mostrar panel de IA"""
        if not self.visible:
            self.ai_frame.pack(side='right', fill='y', padx=(5, 0))
            self.visible = True
            self.input_entry.focus_set()
            
    def hide(self):
        """Ocultar panel de IA"""
        if self.visible:
            self.ai_frame.pack_forget()
            self.visible = False
            
    def add_message(self, sender, message, tag='ai'):
        """Agregar mensaje al chat"""
        self.chat_display.config(state='normal')
        
        # Agregar timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M")
        
        # Agregar mensaje
        self.chat_display.insert(tk.END, f"[{timestamp}] {sender}: ", tag)
        self.chat_display.insert(tk.END, f"{message}\n\n")
        
        # Scroll al final
        self.chat_display.see(tk.END)
        self.chat_display.config(state='disabled')
        
    def add_system_message(self, message):
        """Agregar mensaje del sistema"""
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"💡 {message}\n", 'system')
        self.chat_display.config(state='disabled')
        
    def add_code_block(self, code):
        """Agregar bloque de código"""
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, "\n--- CÓDIGO GENERADO ---\n", 'system')
        self.chat_display.insert(tk.END, f"{code}\n", 'code')
        self.chat_display.insert(tk.END, "--- FIN CÓDIGO ---\n\n", 'system')
        self.chat_display.see(tk.END)
        self.chat_display.config(state='disabled')
        
    def send_message(self, event=None):
        """Enviar mensaje a la IA"""
        message = self.input_var.get().strip()
        if not message:
            return
            
        # Agregar mensaje del usuario
        self.add_message("TÚ", message, 'user')
        self.input_var.set("")
        
        # Procesar con IA
        self.process_ai_request(message)
        
    def process_ai_request(self, message):
        """Procesar solicitud de IA"""
        try:
            from transpilers.ai_assistant import VaderAIAssistant
            
            self.status_label.configure(text="● PROCESANDO...", foreground=self.colors['warning'])
            self.parent.update()
            
            ai = VaderAIAssistant()
            
            # Determinar tipo de solicitud
            message_lower = message.lower()
            
            if any(word in message_lower for word in ['genera', 'crear', 'hacer', 'construir']):
                # Generar código
                codigo = ai.generate_code_from_description(message)
                if codigo:
                    self.add_message("VADER AI", "¡Código generado exitosamente!")
                    self.add_code_block(codigo)
                    
                    # Preguntar si quiere insertarlo en el editor
                    if messagebox.askyesno("Insertar Código", "¿Quieres insertar este código en el editor?"):
                        self.insert_code_in_editor(codigo)
                else:
                    self.add_message("VADER AI", "No pude generar código para esa descripción. ¿Puedes ser más específico?", 'error')
                    
            elif any(word in message_lower for word in ['analiza', 'analizar', 'revisar']):
                # Analizar código del editor
                editor_content = self.get_editor_content()
                if editor_content.strip():
                    analisis = ai.analyze_code(editor_content)
                    self.show_analysis_results(analisis)
                else:
                    self.add_message("VADER AI", "No hay código en el editor para analizar.", 'error')
                    
            elif any(word in message_lower for word in ['optimiza', 'optimizar', 'mejorar']):
                # Optimizar código
                editor_content = self.get_editor_content()
                if editor_content.strip():
                    codigo_optimizado = ai.optimize_code(editor_content)
                    if codigo_optimizado != editor_content:
                        self.add_message("VADER AI", "¡Código optimizado!")
                        self.add_code_block(codigo_optimizado)
                        
                        if messagebox.askyesno("Reemplazar Código", "¿Quieres reemplazar el código actual con la versión optimizada?"):
                            self.replace_editor_content(codigo_optimizado)
                    else:
                        self.add_message("VADER AI", "Tu código ya está bien optimizado. ¡Buen trabajo!")
                else:
                    self.add_message("VADER AI", "No hay código en el editor para optimizar.", 'error')
                    
            elif any(word in message_lower for word in ['errores', 'error', 'bugs', 'problemas']):
                # Buscar errores
                editor_content = self.get_editor_content()
                if editor_content.strip():
                    errores = ai.check_errors(editor_content)
                    if errores:
                        self.add_message("VADER AI", "Encontré algunos problemas:", 'error')
                        for error in errores:
                            self.add_message("", f"• {error}", 'error')
                    else:
                        self.add_message("VADER AI", "¡No encontré errores! Tu código se ve bien.", 'success')
                else:
                    self.add_message("VADER AI", "No hay código en el editor para revisar.", 'error')
                    
            else:
                # Respuesta general
                self.add_message("VADER AI", "Entiendo. Puedo ayudarte con:")
                self.add_message("", "• Generar código: 'genera una calculadora'")
                self.add_message("", "• Analizar código: 'analiza mi código'")
                self.add_message("", "• Optimizar código: 'optimiza este código'")
                self.add_message("", "• Buscar errores: 'busca errores'")
                
            self.status_label.configure(text="● ONLINE", foreground=self.colors['success'])
            
        except ImportError:
            self.add_message("VADER AI", "Sistema de IA no disponible. Verifica la instalación.", 'error')
            self.status_label.configure(text="● ERROR", foreground=self.colors['error'])
        except Exception as e:
            self.add_message("VADER AI", f"Error: {str(e)}", 'error')
            self.status_label.configure(text="● ERROR", foreground=self.colors['error'])
            
    def show_analysis_results(self, analisis):
        """Mostrar resultados del análisis"""
        self.add_message("VADER AI", "📊 Análisis completado:")
        
        if analisis.get('errors'):
            self.add_message("", "❌ ERRORES:", 'error')
            for error in analisis['errors']:
                self.add_message("", f"  • {error}", 'error')
                
        if analisis.get('warnings'):
            self.add_message("", "⚠️ ADVERTENCIAS:", 'error')
            for warning in analisis['warnings']:
                self.add_message("", f"  • {warning}", 'error')
                
        if analisis.get('suggestions'):
            self.add_message("", "💡 SUGERENCIAS:")
            for suggestion in analisis['suggestions']:
                self.add_message("", f"  • {suggestion}")
                
        if 'score' in analisis:
            score = analisis['score']
            color = 'success' if score >= 80 else 'warning' if score >= 60 else 'error'
            self.add_message("", f"📈 Puntuación: {score}/100", color)
            
    def quick_generate(self):
        """Acción rápida: generar código"""
        self.input_var.set("genera un programa simple")
        self.send_message()
        
    def quick_analyze(self):
        """Acción rápida: analizar código"""
        self.input_var.set("analiza mi código")
        self.send_message()
        
    def quick_optimize(self):
        """Acción rápida: optimizar código"""
        self.input_var.set("optimiza mi código")
        self.send_message()
        
    def quick_check_errors(self):
        """Acción rápida: buscar errores"""
        self.input_var.set("busca errores en mi código")
        self.send_message()
        
    def get_editor_content(self):
        """Obtener contenido del editor principal"""
        try:
            # Buscar el editor en la aplicación principal
            root = self.parent
            while root.master:
                root = root.master
            
            # Buscar el editor
            for widget in root.winfo_children():
                if hasattr(widget, 'editor'):
                    return widget.editor.get_content()
            return ""
        except:
            return ""
            
    def insert_code_in_editor(self, code):
        """Insertar código en el editor"""
        try:
            root = self.parent
            while root.master:
                root = root.master
                
            for widget in root.winfo_children():
                if hasattr(widget, 'editor'):
                    current_content = widget.editor.get_content()
                    if current_content.strip():
                        # Agregar al final
                        new_content = current_content + "\n\n# Código generado por IA\n" + code
                    else:
                        # Reemplazar contenido vacío
                        new_content = code
                    widget.editor.set_content(new_content)
                    break
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo insertar el código: {e}")
            
    def replace_editor_content(self, code):
        """Reemplazar contenido del editor"""
        try:
            root = self.parent
            while root.master:
                root = root.master
                
            for widget in root.winfo_children():
                if hasattr(widget, 'editor'):
                    widget.editor.set_content(code)
                    break
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo reemplazar el código: {e}")
