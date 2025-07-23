"""
Framework React para Vader
Transpila código Vader a componentes React con JSX
"""

class ReactFramework:
    def __init__(self):
        self.name = "React"
        self.description = "Framework para crear interfaces de usuario interactivas"
        self.target_language = "javascript"
        self.keywords = ['componente', 'react', 'jsx', 'estado', 'hook', 'usestate', 'useeffect']
    
    def detect(self, code):
        """Detecta si el código usa React"""
        code_lower = code.lower()
        return any(keyword in code_lower for keyword in self.keywords)
    
    def transpile(self, vader_code):
        """Transpila código Vader a React"""
        lines = vader_code.strip().split('\n')
        react_code = []
        
        # Imports básicos de React
        react_code.append("import React, { useState, useEffect } from 'react';")
        react_code.append("")
        
        # Detectar componentes
        component_name = "VaderComponent"
        for line in lines:
            if 'componente' in line.lower():
                # Extraer nombre del componente
                parts = line.split()
                if len(parts) > 1:
                    component_name = parts[1].capitalize()
                break
        
        # Crear componente React
        react_code.append(f"const {component_name} = () => {{")
        
        # Estado inicial
        react_code.append("  const [data, setData] = useState('');")
        react_code.append("  const [loading, setLoading] = useState(false);")
        react_code.append("")
        
        # Procesar líneas de código Vader
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            if 'mostrar' in line.lower() or 'imprimir' in line.lower():
                # Convertir a JSX
                content = line.split('"')[1] if '"' in line else "data"
                react_code.append(f"      <p>{{{content}}}</p>")
            elif 'pedir' in line.lower() or 'input' in line.lower():
                # Convertir a input JSX
                react_code.append("      <input")
                react_code.append("        type='text'")
                react_code.append("        value={data}")
                react_code.append("        onChange={(e) => setData(e.target.value)}")
                react_code.append("        placeholder='Ingresa texto'")
                react_code.append("      />")
        
        # JSX return
        react_code.append("  return (")
        react_code.append("    <div className='vader-component'>")
        react_code.append("      <h1>Componente Vader</h1>")
        
        # Agregar elementos detectados
        has_content = False
        for line in lines:
            line = line.strip()
            if 'mostrar' in line.lower() or 'imprimir' in line.lower():
                content = line.split('"')[1] if '"' in line else "{data}"
                react_code.append(f"      <p>{content}</p>")
                has_content = True
            elif 'pedir' in line.lower() or 'input' in line.lower():
                react_code.append("      <input")
                react_code.append("        type='text'")
                react_code.append("        value={data}")
                react_code.append("        onChange={(e) => setData(e.target.value)}")
                react_code.append("        placeholder='Ingresa texto'")
                react_code.append("      />")
                has_content = True
        
        if not has_content:
            react_code.append("      <p>Componente React generado desde Vader</p>")
        
        react_code.append("    </div>")
        react_code.append("  );")
        react_code.append("};")
        react_code.append("")
        react_code.append(f"export default {component_name};")
        
        return '\n'.join(react_code)
