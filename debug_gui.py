#!/usr/bin/env python3
"""
DEBUG GUI - Versión simplificada para depurar problemas
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

def test_basic_gui():
    """Probar GUI básica"""
    print("🔧 Iniciando debug de GUI...")
    
    try:
        # Crear ventana principal
        root = tk.Tk()
        root.title("VADER GUI - DEBUG")
        root.geometry("800x600")
        root.configure(bg='#000000')  # Negro
        
        print("✅ Ventana principal creada")
        
        # Crear frame principal
        main_frame = tk.Frame(root, bg='#000000')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        print("✅ Frame principal creado")
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="⚡ VADER - DEBUG MODE",
            bg='#000000',
            fg='#00ff41',
            font=('Consolas', 16, 'bold')
        )
        title_label.pack(pady=20)
        
        print("✅ Título agregado")
        
        # Área de texto
        text_area = tk.Text(
            main_frame,
            bg='#111111',
            fg='#ffffff',
            font=('Consolas', 12),
            height=20,
            width=80
        )
        text_area.pack(fill='both', expand=True, pady=10)
        
        # Contenido inicial
        debug_content = """# 🔧 VADER GUI - MODO DEBUG

✅ Ventana principal: OK
✅ Frame principal: OK  
✅ Título: OK
✅ Área de texto: OK

🎨 Colores:
- Fondo: Negro (#000000)
- Texto: Blanco (#ffffff)
- Acento: Verde neón (#00ff41)

Si puedes ver este texto, la GUI básica funciona correctamente.

Próximo paso: Implementar componentes completos.
"""
        
        text_area.insert('1.0', debug_content)
        text_area.config(state='disabled')
        
        print("✅ Contenido agregado")
        
        # Botón de prueba
        test_button = tk.Button(
            main_frame,
            text="🚀 GUI FUNCIONANDO",
            bg='#2d2d2d',
            fg='#00ff41',
            font=('Consolas', 12, 'bold'),
            command=lambda: print("✅ Botón presionado - GUI funcional")
        )
        test_button.pack(pady=10)
        
        print("✅ Botón agregado")
        print("🚀 GUI debug lista - iniciando mainloop...")
        
        # Ejecutar
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ Error en GUI debug: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_basic_gui()
    if success:
        print("✅ Debug GUI completado exitosamente")
    else:
        print("❌ Debug GUI falló")
