#!/usr/bin/env python3
"""
VADER EDITOR - Editor de Código con Sintaxis Highlighting
Diseño: Moderno, Oscuro, Minimalista con Negro Predominante
"""

import tkinter as tk
from tkinter import scrolledtext, font
import re

class VaderEditor:
    """Editor de código Vader con highlighting y características avanzadas"""
    
    def __init__(self, parent, colors):
        self.parent = parent
        self.colors = colors
        # Definir keywords primero
        self.keywords = [
            'funcion', 'fin', 'clase', 'si', 'sino', 'fin si', 'repetir', 'mientras',
            'para', 'en', 'desde', 'hasta', 'mostrar', 'preguntar', 'leer', 'escribir',
            'intentar', 'capturar', 'finalmente', 'lanzar', 'retornar', 'romper',
            'continuar', 'verdadero', 'falso', 'nulo', 'y', 'o', 'no', 'es', 'como',
            'importar', 'de', 'usar', 'plantilla', 'componente', 'con', 'servidor',
            'ruta', 'get', 'post', 'put', 'delete', 'conectar', 'base_datos'
        ]
        self.setup_editor()
        self.setup_syntax_highlighting()
        self.setup_shortcuts()
        
    def setup_editor(self):
        """Configurar el editor de texto"""
        # Frame principal del editor
        self.editor_frame = tk.Frame(self.parent, bg=self.colors['bg_primary'])
        self.editor_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Números de línea
        self.line_numbers = tk.Text(
            self.editor_frame,
            width=4,
            padx=5,
            pady=5,
            takefocus=0,
            border=0,
            state='disabled',
            wrap='none',
            bg=self.colors['bg_secondary'],
            fg=self.colors['fg_secondary'],
            font=('Consolas', 11),
            selectbackground=self.colors['bg_secondary']
        )
        self.line_numbers.pack(side='left', fill='y')
        
        # Editor principal
        self.text_editor = scrolledtext.ScrolledText(
            self.editor_frame,
            wrap='none',
            bg=self.colors['bg_primary'],
            fg=self.colors['fg_primary'],
            font=('Consolas', 11),
            insertbackground=self.colors['fg_accent'],  # Color del cursor
            selectbackground=self.colors['selection'],
            selectforeground=self.colors['fg_primary'],
            borderwidth=1,
            relief='solid',
            highlightcolor=self.colors['fg_accent'],
            highlightthickness=1
        )
        self.text_editor.pack(side='right', fill='both', expand=True)
        
        # Configurar scrollbar oscura
        self.text_editor.vbar.configure(
            bg=self.colors['bg_secondary'],
            troughcolor=self.colors['bg_tertiary'],
            activebackground=self.colors['bg_accent']
        )
        
        # Eventos
        self.text_editor.bind('<KeyRelease>', self.on_content_changed)
        self.text_editor.bind('<Button-1>', self.on_content_changed)
        self.text_editor.bind('<MouseWheel>', self.on_scroll)
        
        # Contenido inicial
        self.set_initial_content()
        
    def setup_syntax_highlighting(self):
        """Configurar resaltado de sintaxis para Vader"""
        # Configurar tags para diferentes elementos
        self.text_editor.tag_configure('keyword', foreground=self.colors['fg_accent'], font=('Consolas', 11, 'bold'))
        self.text_editor.tag_configure('string', foreground='#ffa500')  # Naranja para strings
        self.text_editor.tag_configure('comment', foreground=self.colors['fg_secondary'], font=('Consolas', 11, 'italic'))
        self.text_editor.tag_configure('number', foreground='#87ceeb')  # Azul claro para números
        self.text_editor.tag_configure('function', foreground='#ff69b4')  # Rosa para funciones
        self.text_editor.tag_configure('class', foreground='#98fb98')  # Verde claro para clases
        self.text_editor.tag_configure('variable', foreground='#dda0dd')  # Violeta para variables
        
    def setup_shortcuts(self):
        """Configurar atajos de teclado"""
        self.text_editor.bind('<Control-s>', lambda e: self.parent.master.save_file())
        self.text_editor.bind('<Control-o>', lambda e: self.parent.master.open_file())
        self.text_editor.bind('<F5>', lambda e: self.parent.master.run_code())
        self.text_editor.bind('<Control-slash>', self.toggle_comment)
        
    def set_initial_content(self):
        """Establecer contenido inicial del editor"""
        initial_code = """# ¡Bienvenido a VADER! 🚀
# El Lenguaje Supremo Universal

# Ejemplo básico - Calculadora simple
funcion calculadora
    mostrar "=== CALCULADORA VADER ==="
    
    preguntar "Ingresa el primer número:" guardar la respuesta en num1
    preguntar "Ingresa el segundo número:" guardar la respuesta en num2
    preguntar "Operación (+, -, *, /):" guardar la respuesta en operacion
    
    convertir num1 a numero
    convertir num2 a numero
    
    si operacion es "+"
        resultado = num1 + num2
    sino si operacion es "-"
        resultado = num1 - num2
    sino si operacion es "*"
        resultado = num1 * num2
    sino si operacion es "/"
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

# Ejecutar calculadora
calculadora()

# ¡Presiona F5 para ejecutar o usa el botón ▶️!
# ¡Prueba la IA con el botón 🤖!"""
        
        self.text_editor.delete('1.0', tk.END)
        self.text_editor.insert('1.0', initial_code)
        self.highlight_syntax()
        self.update_line_numbers()
        
    def on_content_changed(self, event=None):
        """Manejar cambios en el contenido"""
        self.highlight_syntax()
        self.update_line_numbers()
        
    def on_scroll(self, event):
        """Sincronizar scroll de números de línea"""
        self.line_numbers.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def highlight_syntax(self):
        """Aplicar resaltado de sintaxis"""
        content = self.text_editor.get('1.0', tk.END)
        
        # Limpiar tags existentes
        for tag in ['keyword', 'string', 'comment', 'number', 'function', 'class', 'variable']:
            self.text_editor.tag_remove(tag, '1.0', tk.END)
        
        # Resaltar comentarios
        for match in re.finditer(r'#.*', content):
            start = self.get_position(content, match.start())
            end = self.get_position(content, match.end())
            self.text_editor.tag_add('comment', start, end)
        
        # Resaltar strings
        for match in re.finditer(r'"[^"]*"', content):
            start = self.get_position(content, match.start())
            end = self.get_position(content, match.end())
            self.text_editor.tag_add('string', start, end)
        
        # Resaltar números
        for match in re.finditer(r'\b\d+\.?\d*\b', content):
            start = self.get_position(content, match.start())
            end = self.get_position(content, match.end())
            self.text_editor.tag_add('number', start, end)
        
        # Resaltar palabras clave
        for keyword in self.keywords:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            for match in re.finditer(pattern, content, re.IGNORECASE):
                start = self.get_position(content, match.start())
                end = self.get_position(content, match.end())
                self.text_editor.tag_add('keyword', start, end)
        
        # Resaltar funciones (palabra seguida de paréntesis)
        for match in re.finditer(r'\b[a-záéíóúñ_][a-záéíóúñ0-9_]*(?=\s*\()', content, re.IGNORECASE):
            start = self.get_position(content, match.start())
            end = self.get_position(content, match.end())
            self.text_editor.tag_add('function', start, end)
        
        # Resaltar definiciones de función
        for match in re.finditer(r'(?<=funcion\s)[a-záéíóúñ_][a-záéíóúñ0-9_]*', content, re.IGNORECASE):
            start = self.get_position(content, match.start())
            end = self.get_position(content, match.end())
            self.text_editor.tag_add('function', start, end)
        
        # Resaltar definiciones de clase
        for match in re.finditer(r'(?<=clase\s)[a-záéíóúñ_][a-záéíóúñ0-9_]*', content, re.IGNORECASE):
            start = self.get_position(content, match.start())
            end = self.get_position(content, match.end())
            self.text_editor.tag_add('class', start, end)
            
    def get_position(self, content, index):
        """Convertir índice de string a posición de tkinter"""
        lines_before = content[:index].count('\n')
        line_start = content.rfind('\n', 0, index) + 1
        column = index - line_start
        return f"{lines_before + 1}.{column}"
        
    def update_line_numbers(self):
        """Actualizar números de línea"""
        content = self.text_editor.get('1.0', tk.END)
        line_count = content.count('\n')
        
        self.line_numbers.config(state='normal')
        self.line_numbers.delete('1.0', tk.END)
        
        for i in range(1, line_count + 1):
            self.line_numbers.insert(tk.END, f"{i:3}\n")
            
        self.line_numbers.config(state='disabled')
        
    def toggle_comment(self, event):
        """Comentar/descomentar línea actual"""
        current_line = self.text_editor.index(tk.INSERT).split('.')[0]
        line_start = f"{current_line}.0"
        line_end = f"{current_line}.end"
        line_content = self.text_editor.get(line_start, line_end)
        
        if line_content.strip().startswith('#'):
            # Descomentar
            new_content = line_content.replace('#', '', 1)
        else:
            # Comentar
            new_content = '# ' + line_content
            
        self.text_editor.delete(line_start, line_end)
        self.text_editor.insert(line_start, new_content)
        
        return 'break'  # Prevenir comportamiento por defecto
        
    def get_content(self):
        """Obtener contenido del editor"""
        return self.text_editor.get('1.0', tk.END + '-1c')
        
    def set_content(self, content):
        """Establecer contenido del editor"""
        self.text_editor.delete('1.0', tk.END)
        self.text_editor.insert('1.0', content)
        self.highlight_syntax()
        self.update_line_numbers()
        
    def clear(self):
        """Limpiar editor"""
        self.text_editor.delete('1.0', tk.END)
        self.update_line_numbers()
        
    def focus(self):
        """Enfocar editor"""
        self.text_editor.focus_set()
